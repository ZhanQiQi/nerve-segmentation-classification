

import torch.nn.functional as F
import torch.nn as nn
from base import BaseModel


class SegNet(BaseModel):

    def __init__(self):

        super(SegNet, self).__init__()

        self.conv1_1 = nn.Conv2d(31, 64, kernel_size=3, stride=1, padding=1)
        self.conv1_2 = nn.Conv2d(64, 64, kernel_size=3, stride=1, padding=1)
        self.conv2_1 = nn.Conv2d(64, 128, kernel_size=3, stride=1, padding=1)
        self.conv2_2 = nn.Conv2d(128, 128, kernel_size=3, stride=1, padding=1)
        self.conv3_1 = nn.Conv2d(128, 256, kernel_size=3, stride=1, padding=1)
        self.conv3_2 = nn.Conv2d(256, 256, kernel_size=3, stride=1, padding=1)
        self.conv3_3 = nn.Conv2d(256, 256, kernel_size=3, stride=1, padding=1)
        self.conv4_1 = nn.Conv2d(256, 512, kernel_size=3, stride=1, padding=1)
        self.conv4_2 = nn.Conv2d(512, 512, kernel_size=3, stride=1, padding=1)
        self.conv4_3 = nn.Conv2d(512, 512, kernel_size=3, stride=1, padding=1)
        self.conv5_1 = nn.Conv2d(512, 512, kernel_size=3, stride=1, padding=1)
        self.conv5_2 = nn.Conv2d(512, 512, kernel_size=3, stride=1, padding=1)
        self.conv5_3 = nn.Conv2d(512, 512, kernel_size=3, stride=1, padding=1)

        self.pool1 = nn.MaxPool2d(
            kernel_size=2, stride=2, padding=0, return_indices=True)
        self.pool2 = nn.MaxPool2d(
            kernel_size=2, stride=2, padding=0, return_indices=True)
        self.pool3 = nn.MaxPool2d(
            kernel_size=2, stride=2, padding=0, return_indices=True)
        self.pool4 = nn.MaxPool2d(
            kernel_size=2, stride=2, padding=0, return_indices=True)
        self.pool5 = nn.MaxPool2d(
            kernel_size=2, stride=2, padding=0, return_indices=True)

        self.unpool5 = nn.MaxUnpool2d(kernel_size=2, stride=2, padding=0)
        self.unpool4 = nn.MaxUnpool2d(kernel_size=2, stride=2, padding=0)
        self.unpool3 = nn.MaxUnpool2d(kernel_size=2, stride=2, padding=0)
        self.unpool2 = nn.MaxUnpool2d(kernel_size=2, stride=2, padding=0)
        self.unpool1 = nn.MaxUnpool2d(kernel_size=2, stride=2, padding=0)

        # to get rid of grid artifacts due to deconv
        self.avgpool1 = nn.AvgPool2d(kernel_size=3, stride=1, padding=1)
        self.sigmoid1 = nn.Sigmoid()
        self.tanh1 = nn.Tanh()

        self.deconv5_1 = nn.ConvTranspose2d(
            512, 512, kernel_size=3, stride=1, padding=1)
        self.deconv5_2 = nn.ConvTranspose2d(
            512, 512, kernel_size=3, stride=1, padding=1)
        self.deconv5_3 = nn.ConvTranspose2d(
            512, 512, kernel_size=3, stride=1, padding=1)
        self.deconv4_1 = nn.ConvTranspose2d(
            512, 512, kernel_size=3, stride=1, padding=1)
        self.deconv4_2 = nn.ConvTranspose2d(
            512, 512, kernel_size=3, stride=1, padding=1)
        self.deconv4_3 = nn.ConvTranspose2d(
            512, 256, kernel_size=3, stride=1, padding=1)
        self.deconv3_1 = nn.ConvTranspose2d(
            256, 256, kernel_size=3, stride=1, padding=1)
        self.deconv3_2 = nn.ConvTranspose2d(
            256, 256, kernel_size=3, stride=1, padding=1)
        self.deconv3_3 = nn.ConvTranspose2d(
            256, 128, kernel_size=3, stride=1, padding=1)
        self.deconv2_1 = nn.ConvTranspose2d(
            128, 128, kernel_size=3, stride=1, padding=1)
        self.deconv2_2 = nn.ConvTranspose2d(
            128, 64, kernel_size=3, stride=1, padding=1)
        self.deconv1_1 = nn.ConvTranspose2d(
            64, 64, kernel_size=3, stride=1, padding=1)
        self.deconv1_2 = nn.ConvTranspose2d(
            64, 2, kernel_size=3, stride=1, padding=1)

        self.batch_norm1 = nn.BatchNorm2d(64)
        self.batch_norm2 = nn.BatchNorm2d(128)
        self.batch_norm3 = nn.BatchNorm2d(256)
        self.batch_norm4 = nn.BatchNorm2d(512)

    def forward(self, x):

        size_1 = x.size()

        ##################################
        x = self.conv1_1(x)  # convolution brings the difference ?!?!?!?
        ##################################

        x = self.batch_norm1(x)

        x = F.relu(x)
        x = self.conv1_2(x)
        x = self.batch_norm1(x)
        x = F.relu(x)
        x, idxs1 = self.pool1(x)


# already different

        size_2 = x.size()
        x = self.conv2_1(x)
        x = self.batch_norm2(x)
        x = F.relu(x)
        x = self.conv2_2(x)
        x = self.batch_norm2(x)
        x = F.relu(x)
        x, idxs2 = self.pool2(x)

        size_3 = x.size()
        x = self.conv3_1(x)
        x = self.batch_norm3(x)
        x = F.relu(x)
        x = self.conv3_2(x)
        x = self.batch_norm3(x)
        x = F.relu(x)
        x = self.conv3_3(x)
        x = self.batch_norm3(x)
        x = F.relu(x)
        x, idxs3 = self.pool3(x)

        size_4 = x.size()
        x = self.conv4_1(x)
        x = self.batch_norm4(x)
        x = F.relu(x)
        x = self.conv4_2(x)
        x = self.batch_norm4(x)
        x = F.relu(x)
        x = self.conv4_3(x)
        x = self.batch_norm4(x)
        x = F.relu(x)
        x, idxs4 = self.pool4(x)

        size_5 = x.size()
        x = self.conv5_1(x)
        x = self.batch_norm4(x)
        x = F.relu(x)
        x = self.conv5_2(x)
        x = self.batch_norm4(x)
        x = F.relu(x)
        x = self.conv5_3(x)
        x = self.batch_norm4(x)
        x = F.relu(x)
        x, idxs5 = self.pool5(x)

        x = self.unpool5(x, idxs5, output_size=size_5)
        x = self.deconv5_1(x)
        x = self.batch_norm4(x)
        x = F.relu(x)
        x = self.deconv5_2(x)
        x = self.batch_norm4(x)
        x = F.relu(x)
        x = self.deconv5_3(x)
        x = self.batch_norm4(x)
        x = F.relu(x)

# already different

        x = self.unpool4(x, idxs4, output_size=size_4)
        x = self.deconv4_1(x)
        x = self.batch_norm4(x)
        x = F.relu(x)
        x = self.deconv4_2(x)
        x = self.batch_norm4(x)
        x = F.relu(x)
        x = self.deconv4_3(x)
        x = self.batch_norm3(x)
        x = F.relu(x)

        x = self.unpool3(x, idxs3, output_size=size_3)
        x = self.deconv3_1(x)
        x = self.batch_norm3(x)
        x = F.relu(x)
        x = self.deconv3_2(x)
        x = self.batch_norm3(x)
        x = F.relu(x)
        x = self.deconv3_3(x)
        x = self.batch_norm2(x)
        x = F.relu(x)

        x = self.unpool2(x, idxs2, output_size=size_2)
        x = self.deconv2_1(x)
        x = self.batch_norm2(x)
        x = F.relu(x)
        x = self.deconv2_2(x)
        x = self.batch_norm1(x)
        x = F.relu(x)

        x = self.unpool1(x, idxs1, output_size=size_1)
        x = self.deconv1_1(x)
        x = self.batch_norm1(x)
        x = F.relu(x)
        x = self.deconv1_2(x)

        #x = self.avgpool1(x)
        #x = self.sigmoid1(x)
        #x = self.tanh1(x)

        return x
