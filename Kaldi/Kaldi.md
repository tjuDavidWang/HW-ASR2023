# 	Kaldi

Weida Wang, 2151300

## Install Kaldi (in Linux)

1. Download the GitHub repository

   ```bash
   git clone https://github.com/kaldi-asr/kaldi
   ```

2. Compile dependent toolkits in kaldi/tools

   Install subversion, automake, autoconf, libtool, g++, zlib, libatal, wget, sox, gfortran

   ```bash
   sudo apt-get install subversion automake autoconf libtool g++ zlib1g-dev libatlas-base-dev wget sox gfortran
   ```

   Install MKL for faster linear algebra computations

   ```bash
   cd tools
   bash extras/install_mkl.sh
   ```

   Continue until the following command runs, and the appearance of the image below indicates that all dependencies are installed:

   ```bash
   extras/check_dependencies.sh
   ```

   ![image-20231130091814024](C:\Users\12920\AppData\Roaming\Typora\typora-user-images\image-20231130091814024.png)

   Speed up the compilation of `kaldi/tools` using multiple processes:

   ```bash
   make -j 4
   ```

   Install openfst

   ```bash
   make openfst
   ```

3. Compile Kaldi's core libraries `kaldi/src`

   Run the configuration script

   ```bash
   cd ../src
   ./configure --shared
   ```

   The final compilation

   ```bash
   make depend -j 4
   make -j 4
   ```

## Run yesno and THCHS-30 examples

### Test yes/no example

Requires internet connection as it involves downloading a small amount of data

```bash
cd ../egs/yesno/s5
sh run.sh
```

![image-20231130100203446](C:\Users\12920\AppData\Roaming\Typora\typora-user-images\image-20231130100203446.png)

If the run is successful, the WER (Word Error Rate) metric will appear as shown in the following image:

![image-20231130100402583](C:\Users\12920\AppData\Roaming\Typora\typora-user-images\image-20231130100402583.png)

### Test THCHS-30 example

1. Download thchs30 from https://www.openslr.org/18/.

   ![image-20231202232855145](C:\Users\12920\AppData\Roaming\Typora\typora-user-images\image-20231202232855145.png)

2. Since I am using a cloud server on AutoDL, it is necessary to upload the data from the local machine to the cloud server. I recommend using AutoPannal for uploading, it's super fast! As shown in the following image：[Link](https://www.autodl.com/docs/netdisk/)

   <img src="C:\Users\12920\AppData\Roaming\Typora\typora-user-images\image-20231130233145731.png" alt="image-20231130233145731" style="zoom: 67%;" />

   Then use the following command to unzip the three tar packages into one folder

   ```bash
   sudo tar -zxvf /root/autodl-tmp/resource.tgz
   ```

3. Since we are training on a single machine and not on an Oracle GridEngine cluster, change all queues in `egs/thchs30/s5/cmd.sh` to run

   ```sh
   export train_cmd=run.pl
   export decode_cmd="run.pl --mem 4G"
   export mkgraph_cmd="run.pl --mem 8G"
   export cuda_cmd="run.pl --gpu 1"
   ```

4. Modify the number of parallel jobs in `run.sh`

   ```sh
   n=8      #parallel jobs 原则上要小于0.7*物理cpu数*单cpu核数
   ```

   Modify the path in `run.sh` to match the location of our dataset

   ```sh
   # thchs=/nfs/public/materials/data/thchs30-openslr
   # my dataset root: /root/autodl-tmp/data_thchs30
   thchs=/root/autodl-tmp/thchs30
   ```

   According the referenced PPT，we just need to test these four models and `comment` the rest tests in run.sh.

   ![image-20231203003621708](C:\Users\12920\AppData\Roaming\Typora\typora-user-images\image-20231203003621708.png)

5. Check the experimental results

   It is recommended to redirect the output from the terminal to a log file with the following code at the beginning of `run.sh`:

   ```sh
   exec > >(tee log.log) 2>&1
   ```

   - **Monophone Training**

     The end of the monophone training output summarizes the completion of the monophone model training and provides statistics such as the average alignment probability, total training time, percentages of retries and failures, as well as the number of states and Gaussian mixtures.

     ```sh
     exp/mono: nj=8 align prob=-100.09 over 25.49h [retry=0.2%, fail=0.0%] states=656 gauss=989
     ```

     ![image-20231203002702923](C:\Users\12920\AppData\Roaming\Typora\typora-user-images\image-20231203002702923.png)

   - **Triphone Training**

     ```sh
     exp/tri1: nj=8 align prob=-96.75 over 25.49h [retry=0.3%, fail=0.0%] states=1664 gauss=10023 tree-impr=4.80
     ```

     ![image-20231203112848202](C:\Users\12920\AppData\Roaming\Typora\typora-user-images\image-20231203112848202.png)

   - **LDA+MLLT Training**

     ```sh
     exp/tri2b: nj=8 align prob=-48.18 over 25.48h [retry=0.6%, fail=0.0%] states=2064 gauss=15038 tree-impr=4.32 lda-sum=23.97 mllt:impr,logdet=1.21,1.71
     ```

     ![image-20231203113002776](C:\Users\12920\AppData\Roaming\Typora\typora-user-images\image-20231203113002776.png)

   - **SAT Training**

     ```sh
     exp/tri3b: nj=8 align prob=-47.92 over 25.48h [retry=0.5%, fail=0.0%] states=2096 gauss=15025 fmllr-impr=2.43 over 18.95h tree-impr=6.43
     ```

     ![image-20231203113033587](C:\Users\12920\AppData\Roaming\Typora\typora-user-images\image-20231203113033587.png)

## Recognize my own speech

1. Install PortAudio

   ```shell
   cd tools
   ./install_portaudio.sh
   ```

   安装成功显示如下：

   ![image-20231203121515954](C:\Users\12920\AppData\Roaming\Typora\typora-user-images\image-20231203121515954.png)

2. Compile Related Tools:

   When the compilation is complete, it should display `Done`

   ```shell
   cd ..
   cd src
   make ext
   ```

3. Record Your Own Audio:

   You can use the provided Python code to record your audio and generate your `mine.wav` file. Make sure you have the required libraries installed.

   ```python
   import pyaudio
   import wave
   
   def record_audio(output_filename="output.wav", record_seconds=3):
       # Basic parameter settings
       CHUNK = 1024  # Number of frames per buffer
       FORMAT = pyaudio.paInt16  # Size and format of each sample
       CHANNELS = 1  # Number of audio channels (1 for mono, 2 for stereo)
       RATE = 16000   # Sampling rate in Hz
   
       p = pyaudio.PyAudio()
   
       # Start recording
       print("Recording started...")
       stream = p.open(format=FORMAT,
                       channels=CHANNELS,
                       rate=RATE,
                       input=True,
                       frames_per_buffer=CHUNK)
   
       frames = []
   
       for _ in range(0, int(RATE / CHUNK * record_seconds)):
           data = stream.read(CHUNK)
           frames.append(data)
   
       print("Recording finished")
   
       # Stop recording
       stream.stop_stream()
       stream.close()
       p.terminate()
   
       # Save as a WAV file
       wf = wave.open(output_filename, 'wb')
       wf.setnchannels(CHANNELS)
       wf.setsampwidth(p.get_sample_size(FORMAT))
       wf.setframerate(RATE)
       wf.writeframes(b''.join(frames))
       wf.close()
   
       print(f"Audio saved as {output_filename}")
   
   if __name__ == "__main__":
       record_audio("mine.wav", 10)
   
   ```

4. Modify the Script `oneline_demo/run.sh`

   - Comment out the file downloading section 

     ```sh
     #if [ ! -s ${data_file}.tar.bz2 ]; then
     #    echo "Downloading test models and data ..."
     #    wget -T 10 -t 3 $data_url;
     
     #    if [ ! -s ${data_file}.tar.bz2 ]; then
     #        echo "Download of $data_file has failed!"
     #        exit 1
     #    fi
     #fi
     ```

   - Change the acoustic model type  `ac_model_type` to `tri1`。

     ```sh
     ac_model_type=tri1
     ```

   - Modify the recognition code to use your recorded audio:

     ```sh
     simulated)
         echo
         echo -e "  SIMULATED ONLINE DECODING - pre-recorded audio is used\n"
         echo "  The (bigram) language model used to build the decoding graph was"
         echo "  estimated on an audio book's text. The text in question is"
         echo "  \"King Solomon's Mines\" (http://www.gutenberg.org/ebooks/2166)."
         echo "  The audio chunks to be decoded were taken from the audio book read"
         echo "  by John Nicholson(http://librivox.org/king-solomons-mines-by-haggard/)"
         echo
         echo "  NOTE: Using utterances from the book, on which the LM was estimated"
         echo "        is considered to be \"cheating\" and we are doing this only for"
         echo "        the purposes of the demo."
         echo
         echo "  You can type \"./run.sh --test-mode live\" to try it using your"
         echo "  own voice!"
         echo
         mkdir -p $decode_dir
         # make an input .scp file
         > $decode_dir/input.scp
         for f in $audio/*.wav; do
             bf=`basename $f`
             bf=${bf%.wav}
             echo $bf $f >> $decode_dir/input.scp
         done
     #    online-wav-gmm-decode-faster --verbose=1 --rt-min=0.8 --rt-max=0.85\
     #        --max-active=4000 --beam=12.0 --acoustic-scale=0.0769 \
     #        scp:$decode_dir/input.scp $ac_model/model $ac_model/HCLG.fst \
     #        $ac_model/words.txt '1:2:3:4:5' ark,t:$decode_dir/trans.txt \
     #        ark,t:$decode_dir/ali.txt $trans_matrix;;
         online-wav-gmm-decode-faster  --verbose=1 --rt-min=0.8 --rt-max=0.85 --max-active=4000 \
            --beam=12.0 --acoustic-scale=0.0769 --left-context=3 --right-context=3 \
            scp:$decode_dir/input.scp $ac_model/final.mdl $ac_model/HCLG.fst \
            $ac_model/words.txt '1:2:3:4:5' ark,t:$decode_dir/trans.txt \
            ark,t:$decode_dir/ali.txt $trans_matrix;;
     ```

5. Create Directory Structure and Sync Recognition Model:

   1. Copy the "online_demo" directory from "voxforge" to the same level as "thchs30/s5".

   2. Inside the "online_demo" directory, create "online-data" and "work" directories.

   3. Inside "online-data," create "audio" and "models" directories.

      - Place the audio file you want to recognize (i.e., "mine.wav") inside the "audio" directory.

      - Inside the "models" directory, create a "tri1" directory.

        Copy the following files from "s5/exp/tri1" to your "tri1" directory: `final.mdl` and `35.mdl`

        Copy the following files from "s5/exp/tri1/graph_word" to your "tri1" directory: `words.txt` and `HCLG.fst`

      Your directory structure should resemble the one you provided.

   <img src="C:\Users\12920\AppData\Roaming\Typora\typora-user-images\image-20231203124126416.png" alt="image-20231203124126416" style="zoom:50%;" />

5. Perform Testing:

   In the terminal, run the following command to perform testing:

   Please note that the recognition accuracy may not be very high, and the recognized text may contain errors.

   My input is “*语音识别第三次作业。静夜思，床前明月光，疑是地上霜，举头望明月，低头思故乡。*”, while output is:

   ![image-20231203123532827](C:\Users\12920\AppData\Roaming\Typora\typora-user-images\image-20231203123532827.png)