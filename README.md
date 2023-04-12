# Image Compression

## Introduction

On a human scale things happen very quickly. The speed of transmission is generally used to designate the exchange of information between computers or in general electronic devices as transmitter-telecommunications receiver and is considered a performance factor of the telecommunications system or electronic hardware device, particularly felt by the user as a Quality of Service parameter.

Compressed data is ubiquitous in the files you use frequently. For example, without data compression, a 4-minute song could be larger than 150 MB. Similarly, a 5-minute video would have a size that approaches 1 GB or more.

As part of this project, we are going to propose a new compression format, called IRM, which uses a compression method that involves encoding by [RLE](https://github.com/SDAllouche/compression-algorithms) ranges, [Huffman](https://github.com/SDAllouche/compression-algorithms), bit plane slicing and proposing a newhead that will try to overcome the maximum of limitations found on the various compression formats, existing on the market.

## Bit Plane Slicing

Binary plane cutting is a well-known technique used in image processing. Precisely in image compression. It consists of converting an image into a binary image at several levels.

The gray level of each pixel in a digital image is stored as one or more bytes in a computer.
For an 8-bit image, 0 is coded as 00000000 and 255 is coded as 11111111. Any number between 0 and 255 is coded as a byte.
* The leftmost bit is called the most significant bit (MSB) because a change to this bit would significantly change the value encoded by the byte.
* The far right bit is called the least significant bit (LSB), because a change of this bit does not change the coded gray value much.

Or the following table that represents values of part of the pixels of an image:

![image](https://user-images.githubusercontent.com/102489525/231553551-fb273dd7-d2f1-4eb8-b0f7-5d4cc564cba3.png)

These can be represented in binary as follows:

![image](https://user-images.githubusercontent.com/102489525/231553586-2f8daa64-d5a4-4d8b-a91b-99b6a95101ac.png)

These 8-bit pixel values of our image will be represented in a single bit per plane in 8 planes.
Plane 1 contains the least significant bit order among all pixels in the image, and plane 8 contains the most significant bit order among all pixels in the image.
The binary cut-out is shown in the image below:

![image](https://user-images.githubusercontent.com/102489525/231553610-835e1dff-d9ab-4cd0-a138-9793162779a0.png)


## Schema

Concerning the coding, first and to convert a given image, we proceed by a binary transformation of the latter to apply the splitting of the binary plan, then we apply the RLE, which in turn gives a list containing the repetitions (occurrences) bits of the image obtained after the ‘Bit plane slicing’.

Second, and by transforming each occurrence in the list obtained by the RLE into a character, we apply Huffman’s coding, the latter returns us a binary sequence with a reduced size compared to the initial.

![image](https://user-images.githubusercontent.com/102489525/231554403-daa1f3f0-b5ea-449a-8001-b6f547c0c4e4.png)

## License

[MIT License](License)


