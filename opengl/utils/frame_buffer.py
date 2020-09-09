from OpenGL.GL import (GL_COLOR_ATTACHMENT0, GL_DEPTH_ATTACHMENT,
                       GL_DEPTH_COMPONENT, GL_FRAMEBUFFER,
                       GL_FRAMEBUFFER_COMPLETE, GL_NEAREST, GL_RENDERBUFFER,
                       GL_RGB, GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER,
                       GL_TEXTURE_MIN_FILTER, GL_UNSIGNED_BYTE,
                       glBindFramebuffer, glBindRenderbuffer, glBindTexture,
                       glCheckFramebufferStatus, glFramebufferRenderbuffer,
                       glFramebufferTexture2D, glGenFramebuffers,
                       glGenRenderbuffers, glGenTextures,
                       glRenderbufferStorage, glTexImage2D, glTexParameteri)


def initialize_framebuffer_object(width: int, height: int):

    # Create a texture buffer
    rendered_texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, rendered_texture)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, None)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glBindTexture(GL_TEXTURE_2D, 0)

    # Create a render buffer
    # depth_render_buffer = glGenRenderbuffers(1)
    # glBindRenderbuffer(GL_RENDERBUFFER, depth_render_buffer)
    # glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT, width, height)
    # glBindRenderbuffer(GL_RENDERBUFFER, 0)

    # Create a framebuffer and add the handlers
    frame_buffer_object = glGenFramebuffers(1)
    glBindFramebuffer(GL_FRAMEBUFFER, frame_buffer_object)
    glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, rendered_texture, 0)
    # glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_RENDERBUFFER, depth_render_buffer)

    if glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE:
        raise RuntimeError("Frame buffer binding failed. GPU probably does not suppert this FBO config.")

    glBindFramebuffer(GL_FRAMEBUFFER, 0)

    return frame_buffer_object
