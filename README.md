# SoccerNet Ball Action Spotting Challenge (reimplementing the 2023 solution)

## Overview
The [SoccerNet Ball Action Spotting Challenge 2023](https://www.soccer-net.org/challenges/2023#h.vverf0niv2is) aims to identify and analyze salient actions occurring in broadcast soccer games. This task, known as action spotting, involves detecting the timing and type of ball-related actions within videos, addressing the broader challenge of retrieving moments with specific semantic meanings in long, untrimmed video content.

## Our Task
Ball action spotting focuses on identifying both the timing and type of ball-related actions across a set of predefined classes. Each action is marked by a single timestamp, allowing for precise identification of events. Our dataset features a higher density of actions compared to previous challenges, enhancing the complexity and richness of the task.

## Action Classes
We have annotations for various types of soccer ball actions. Initially, the dataset includes two classes: 
- **Pass**
- **Drive**


## Data
The dataset consists of 7 videos from English Football League games, each broadcast in 720p quality. To encourage the development of end-to-end methods, extracted features are not provided. The challenge set is composed of 2 separate games. Additionally, we are allowed to leverage the 500 unannotated games from the Action Spotting challenge as a resource for this task.

## Evaluation Metric
Unlike the [SoccerNet Action Spotting Challenge](https://www.soccer-net.org/challenges/2023#h.x9nb4u9m441u), the actions are much more densely allocated and should be predicted more accurately (with a 1-second precision).


## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.