# -*- coding: utf-8 -*
from loguru import logger

import torch
import torch.nn as nn

from videoanalyst.model.backbone.backbone_base import (TRACK_BACKBONES,
                                                       VOS_BACKBONES)
from videoanalyst.model.common_opr.common_block import conv_bn_relu
from videoanalyst.model.module_base import ModuleBase
from videoanalyst.utils import md5sum


@VOS_BACKBONES.register
@TRACK_BACKBONES.register
class AlexNet(ModuleBase):
    r"""
    AlexNet

    Hyper-parameters
    ----------------
    pretrain_model_path: string
        Path to pretrained backbone parameter file,
        Parameter to be loaded in _update_params_
    """
    default_hyper_params = {"pretrain_model_path": ""}

    def __init__(self):
        super(AlexNet, self).__init__()
        self.conv1 = conv_bn_relu(3, 96, stride=2, kszie=11, pad=0)
        self.pool1 = nn.MaxPool2d(3, 2, 0, ceil_mode=True)
        self.conv2 = conv_bn_relu(96, 256, 1, 5, 0)
        self.pool2 = nn.MaxPool2d(3, 2, 0, ceil_mode=True)
        self.conv3 = conv_bn_relu(256, 384, 1, 3, 0)
        self.conv4 = conv_bn_relu(384, 384, 1, 3, 0)
        self.conv5 = conv_bn_relu(384, 256, 1, 3, 0, has_relu=False)

    def forward(self, x):
        x = self.conv1(x)
        x = self.pool1(x)
        x = self.conv2(x)
        x = self.pool2(x)
        x = self.conv3(x)
        x = self.conv4(x)
        x = self.conv5(x)
        return x

    def update_params(self):
        model_file = self._hyper_params["pretrain_model_path"]
        if model_file != "":
            state_dict = torch.load(model_file,
                                    map_location=torch.device("cpu"))
            self.load_state_dict(state_dict, strict=False)
            logger.info("Load pretrained AlexNet parameters from: %s" %
                        model_file)
            logger.info("Check md5sum of pretrained AlexNet parameters: %s" %
                        md5sum(model_file))
