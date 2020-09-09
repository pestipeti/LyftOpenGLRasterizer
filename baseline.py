import cv2
import numpy as np
import torch

from l5kit.configs import load_config_data
from l5kit.data import ChunkedDataset, LocalDataManager
from l5kit.dataset import AgentDataset
from l5kit.rasterization.rasterizer_builder import (_load_metadata, get_hardcoded_world_to_ecef)
from OpenGL.GLUT import *
from opengl_rasterizer import OpenGLSemanticRasterizer
from torch.utils.data import DataLoader
from torch.utils.data._utils.collate import default_collate
from tqdm import tqdm


def lyft_collate_fn(batch):

    element = batch[0]

    rasterizer_args = [
        "image",
        "agents",
        "selected_agent",
        "history_frames",
        "history_agents",
        "history_tl_faces"
    ]

    result = {
        key: default_collate([d[key] for d in batch]) for key in element if key not in rasterizer_args
    }

    for element in batch:

        for rasterizer_arg in rasterizer_args:

            if rasterizer_arg not in result:
                result[rasterizer_arg] = []

            result[rasterizer_arg].append(element[rasterizer_arg])

    return result


if __name__ == '__main__':
    os.environ["L5KIT_DATA_FOLDER"] = "./input"
    config_file = "baseline_agent_motion.yaml"
    cfg = load_config_data(f"./configs/{config_file}")

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    dm = LocalDataManager()
    dataset_path = dm.require(cfg["train_data_loader"]["key"])
    zarr_dataset = ChunkedDataset(dataset_path)
    zarr_dataset.open()

    raster_cfg = cfg["raster_params"]
    semantic_map_filepath = dm.require(raster_cfg["semantic_map_key"])
    try:
        dataset_meta = _load_metadata(raster_cfg["dataset_meta_key"], dm)
        world_to_ecef = np.array(dataset_meta["world_to_ecef"], dtype=np.float64)
    except (KeyError, FileNotFoundError):
        world_to_ecef = get_hardcoded_world_to_ecef()

    rast = OpenGLSemanticRasterizer(
        raster_size=raster_cfg["raster_size"],
        pixel_size=raster_cfg["pixel_size"],
        ego_center=raster_cfg["ego_center"],
        filter_agents_threshold=0.5,
        history_num_frames=0,
        semantic_map_path=semantic_map_filepath,
        world_to_ecef=world_to_ecef,
    )
    dataset = AgentDataset(cfg, zarr_dataset, None)

    train_dataloader = DataLoader(dataset,
                                  collate_fn=lyft_collate_fn,
                                  shuffle=False,
                                  batch_size=32,
                                  num_workers=4)

    tr_it = iter(train_dataloader)

    for itr in tqdm(range(100)):

        try:
            data = next(tr_it)
        except StopIteration:
            tr_it = iter(train_dataloader)
            data = next(tr_it)

        batch_num = len(data["image"])
        data["image"] = []

        for i in range(batch_num):
            image = rast.rasterize(
                history_frames=data["history_frames"][i],
                history_agents=data["history_agents"][i],
                history_tl_faces=data["history_tl_faces"][i],
                agent=data["selected_agent"][i],
                agents=data["agents"][i]
            )

            image = torch.from_numpy(image)
            data["image"].append(image)

        data["image"] = torch.stack(data["image"])

        # Saving test image
        if itr == 0:
            i = 10
            img = data['image'][i]
            img = img.numpy().transpose(1, 2, 0)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            cv2.imwrite(f"./cache/test_img_{itr}_{i}.png", (img * 255).astype(np.uint8))

        data["image"] = data["image"].to(device)
        data["target_positions"] = data["target_positions"].to(device)
        data["target_availabilities"] = data["target_availabilities"].unsqueeze(-1).to(device)

        # ...your training code goes here...
        # break