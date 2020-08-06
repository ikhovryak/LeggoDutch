# PyTorchHackathon

# Testing commands
- CharNet: 
    > python tools/test_net.py configs/icdar2015_hourglass88.yaml <images_dir> <results_dir>

- deep-text-recognition
    > CUDA_VISIBLE_DEVICES=0 python3 demo.py \
    > --Transformation TPS --FeatureExtraction ResNet --SequenceModeling BiLSTM --Prediction Attn \
    > --image_folder demo_image/ \
    > --saved_model TPS-ResNet-BiLSTM-Attn.pth

    Arguments
    >--train_data: folder path to training lmdb dataset.
    >--valid_data: folder path to validation lmdb dataset.
    >--eval_data: folder path to evaluation (with test.py) lmdb dataset.
    >--select_data: select training data. default is MJ-ST, which means MJ and ST used as training data.
    >--batch_ratio: assign ratio for each selected data in the batch. default is 0.5-0.5, which means 50% of the batch is filled with MJ and the other 50% of the batch is filled ST.
    >--data_filtering_off: skip data filtering when creating LmdbDataset.
    >--Transformation: select Transformation module [None | TPS].
    >--FeatureExtraction: select FeatureExtraction module [VGG | RCNN | ResNet].
    >--SequenceModeling: select SequenceModeling module [None | BiLSTM].
    >--Prediction: select Prediction module [CTC | Attn].
    >--saved_model: assign saved model to evaluation.
    >--benchmark_all_eval: evaluate with 10 evaluation dataset versions, same with Table 1 in our paper.

- CRAFT Text Detection
    >pip install -r requirements.txt
    >python test.py --trained_model=[weightfile] --test_folder=[folder path to test images]

    Arguments
    >--trained_model: pretrained model
    >--text_threshold: text confidence threshold
    >--low_text: text low-bound score
    >--link_threshold: link confidence threshold
    >--cuda: use cuda for inference (default:True)
    >--canvas_size: max image size for inference
    >--mag_ratio: image magnification ratio
    >--poly: enable polygon type result
    >--show_time: show processing time
    >--test_folder: folder path to input images
    >--refine: use link refiner for sentense-level dataset
    >--refiner_model: pretrained refiner model