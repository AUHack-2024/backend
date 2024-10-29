# Video change detection and evaluation

## Overview

Imagine the security worker who works at some factory or other place that doesn't expect guests to come by.
It should be pretty hard for him to follow tens or even hundreds of cameras at a time. Mosts of them are probably static and the picture is not changed for hours. That is where our smart tool can help a lot.

## How does it work?

1. The frames in a video are processed and saved (different params can be customized).
2. Different adjustments like colour filtering, luminance normalization and others are applied on frames.
3. The frames matrix are compared, the differences evaluated.
4. Based on the result of a previous step, the special value `score` that indicates the difference of frames pair is returned (1 - there is not difference, 0 - there is probably no single pixel that matches).
5. All the frames are grouped, the average score for each group is compared - the smallest is returned.
6. All the frames among the best group index are sent to all ws clients.
7. The frames and corresponding to them scores are saved in a history view.
8. The video with the best group of frames is generated.

## Improvements

There is big amount of work that can be done in order to optimize computations efficiency and speed of sending the images.

- **`clients` variable in ws server is a shared resource therefore it should be accessed only within a lock**
- **create multiple threads for each video. Frame extractor object should be created for each thread**
- before actually attempting to send an image the check could be made to ensure any client is connected and ready to receive data (images)
    - this can be achieved by queueing messages. And as soon as any client connects to the server - release all message one by one.
    - add acknowledgment handler in the server. This can help to make sure client actually manages to get and processes data.
