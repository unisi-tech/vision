<h1> CV Tools is a vision system for end users. </h1> 

The task of creating an image classifier based on a user dataset is a common task for an AI programmer, but I haven’t come across an automatic tool that solves the problem without the participation of a programmer.

 CV tools is a visual information analysis service that includes tools for setting up and testing the necessary tasks for a non-programmer; it also allows you to use the trained system as a REST server for image analysis and multi-user support.

At the top there is a system menu; clicking on the elements opens the corresponding screen.


![image](https://github.com/Claus1/cvtools/assets/1247062/bb558b0a-d6d2-40ea-9eb9-26144c28d32c)

<h2> Dataset  </h2>

![image](https://github.com/Claus1/cvtools/assets/1247062/1e369e73-359b-43de-ac76-36bafbff9ffd)


	The dataset editor allows you to add and delete groups and group images to the system dataset.

	Group images fall into the following categories:

	**Group** - images confirmed by the user and reliably reflecting membership in the group. Only images with this status are used when training the visual system.

	**New** - images downloaded from Google Photos at the request of the user and requiring further viewing and changing the status to Group or Deleted.

	**Deleted** - images defined by the user as not belonging to the group. They are stored in the system for possible revision and to avoid repeated downloading and analysis. The system will not offer to reconsider an image previously rated by the user if it appears in the search results again.

	Editing groups.


![image](https://github.com/Claus1/cvtools/assets/1247062/fd972608-01b7-4adc-82aa-7c00a712f8a6)
  

	Adding a group. A root or child group can be created.


![image](https://github.com/Claus1/cvtools/assets/1247062/e9508faf-fb0f-43a6-897b-f7adbf62106b)


	Renaming a group.


![image](https://github.com/Claus1/cvtools/assets/1247062/f79e6d70-afe9-4414-9d6c-038e367964d3)
   Delete a group.

    Editing images of Dataset groups. 

	You can add images to any group. To do this, it makes sense to go to Google in the Images section in your browser and select a query for which Google will show the most relevant images for the desired group.


![image](https://github.com/Claus1/cvtools/assets/1247062/5531536d-ed5a-4c71-8a73-e93e58d545c9)

After that, in the Vision dataset window, select the group in the list of groups to which you want to add images and click
![image](https://github.com/Claus1/cvtools/assets/1247062/1665d4e3-45c3-4eb4-b0cb-8c0a47cfad1a)
 and it will appear


![image](https://github.com/Claus1/cvtools/assets/1247062/979a167f-b6d2-493f-b08b-514150b921af)


In this dialog you need to enter the selected query, the system will download all the images, add and open them in the New section.

After this, the user must view and select the images by clicking on each one to transfer to the Group or Deleted sections.


![image](https://github.com/Claus1/cvtools/assets/1247062/8cb1d9cf-7ab1-4348-bacb-ab34f5a42dc8)


Buttons
![image](https://github.com/Claus1/cvtools/assets/1247062/f34d9ea8-6534-4671-96f9-aa720c475e34)
 transfer selected images from the New section to the Group or Deleted sections.

Button
![image](https://github.com/Claus1/cvtools/assets/1247062/0cc94b64-20e6-41d5-a499-599198405982)

 changes the image selection status to the opposite for all displayed images.

If you need to take a closer look at the image, clicking on the square with the number in the image brings up the image lens.

![image](https://github.com/Claus1/cvtools/assets/1247062/93ba45c4-7191-4447-b76e-f4f8a4b430c0)



Selecting group sections is done by clicking on the switch
![image](https://github.com/Claus1/cvtools/assets/1247062/b0a166f7-6ea9-40c1-b51d-0da97afd27fd)

<h2>			Training the system (neural network).</h2>


![image](https://github.com/Claus1/cvtools/assets/1247062/09ca582c-e705-4b6d-b836-8a7db963f85e)


At this screen the system is trained using Dataset data. The training parameters have values ​​close to optimal, but can be changed and selected by the user to achieve maximum accuracy of the neural network. Detailed information about the meaning and meaning of these parameters can be found here [https://huggingface.co/docs/transformers/main_classes/trainer#transformers.TrainingArguments](https://huggingface.co/docs/transformers/main_classes/trainer#transformers.TrainingArguments) The user does not need to understand the meaning and meaning of these parameters.





Start learning process. The learning progress is displayed in the Epochs table.


![image](https://github.com/Claus1/cvtools/assets/1247062/bcbe861a-4bbd-40ce-9e99-7347d10e552a)


The neural network is trained to achieve maximum accuracy.` During training, the system is not available for use by other users and systems.` 

The accuracy of the resulting neural network for each training iteration is shown in the column **Accuracy.**

The resulting network with maximum Accuracy can be saved and assigned in the system as the main one (Production)
![image](https://github.com/Claus1/cvtools/assets/1247062/62b8496b-2955-42fe-9df1-b3c8b3523016)


**After appointment** the neuronetwork, you can try to improve the accuracy of it:

1. Changing training parameters. To do this, you need at least a superficial understanding of the parameters and learning process of the neural network.
2. Improve the quality of training data - Dataset.

    To do this, you need to find and correct anomalies in the data, for which the Anomalies section is intended.

    There are 2 types of anomalies:

1. Group detection errors when the neural network incorrectly determines the group of an image. To do this, in Anomalies you need to select the Errors type and click the button
![image](https://github.com/Claus1/cvtools/assets/1247062/02830c99-8931-44dc-863d-0a66ff65725b)
 A list will appear


![image](https://github.com/Claus1/cvtools/assets/1247062/f23ebff1-6fef-40b2-a09a-b71771db79f9)


 Which shows incorrectly identified images. In the description of the image, the first is the erroneous group and its probability, the second is the real group of the image and its probability. For erroneous images, the probability of an erroneous group is greater than the probability of a correct and expected one.

	For erroneously detected images, the following actions are provided:



 Transferring a image from the current group to another ‘correct’ one


![image](https://github.com/Claus1/cvtools/assets/1247062/b51af6fa-956f-4db0-844d-c34a9d1166eb)
.

**	**To do this, select the desired images to transfer and press the button
![image](https://github.com/Claus1/cvtools/assets/1247062/8739503e-bd77-4a0a-b45e-b886061cb7f7)
 and select the group where to transfer.



2. Removing erroneously detected images.

    If an image does not correspond to the group it is in, and the other groups are not suitable for it, then it is better to delete such an image. To do this, click each such image and press
![image](https://github.com/Claus1/cvtools/assets/1247062/94345d86-f09f-497e-b664-be7d3a154d2a)
.


      The second type of anomalies are the same or very similar images, for example, of poorer quality or cropping of one image. Such images have almost no effect on the quality of analysis for datasets with more than 30 images in a group, however, for small datasets, the individual characteristics of duplicate images can have a negative impact on the quality of analysis. To search for duplicates in Anomalies you need to select Type -> Duplicates and click the button
![image](https://github.com/Claus1/cvtools/assets/1247062/0fa26706-07a6-49fb-b5c1-77638d6823b8)
 A list will appear


![image](https://github.com/Claus1/cvtools/assets/1247062/ac85e006-a723-4e99-a5d6-ac783b5740d8)


The images in the list come in pairs and the first digit in the caption of the image is the number of the pair.

Next comes the groups of images and the distance to the other image of the pair. The smaller the distance, the less the images differ from each other. The same transfer and deletion operations are available for images as for incorrectly identified ones. It makes sense to remove duplicates, especially when they are in different groups.


<h2>Analysis of the visual system for images.</h2>

**	**Allows you to test the output of a trained neural network and calculate the most similar images of groups. Similar images make it possible to understand why the classifier’s response is as follows: adjust the Dataset and get a better result on the corrected Dataset.


![image](https://github.com/Claus1/cvtools/assets/1247062/586d5629-8de2-45b4-9586-1f6fd8721c9a)


To upload an image you need to drag it onto the button
![image](https://github.com/Claus1/cvtools/assets/1247062/a6e051a4-2171-4ec1-9c7c-42b273316e35)


or click on + there. When clicked, a file selection dialog will appear in which you need to select an image and click OK.

Information about the groups and their probabilities recognized by the neural network will appear in the Image classification table. When you select any group, images from this category will appear in the table with a distance in ~n-dimensional neural network space to each image in the Similar images block, where n is the number of groups in the Dataset.

The data in the table is as follows:

_Group - group_ Dataset.

_Probability - the analyzer’s confidence (probability) that the image belongs to this group.	_

Additional settings:

	The Search switch, when active, activates the search for similar images.

	How many images to search tells the system exactly how many similar images it should show in descending order of similarity.

<h2>		How to use the CV Tools program.</h2>


0. Install dependencies.

            Install pytorch according to the instructions [https://pytorch.org/get-started/locally/](https://pytorch.org/get-started/locally/)

            Install dependent packages:


    -Go to the working directory of CV Tools


    -execute command `pip install -U -r requirements.txt`



1. Setting up the program.

    All program settings are stored in the config.py file and must be made before starting the program.


    ```
    dataset_dir
    	Defines the full or relative path to the directory where the user dataset is located.

    neuronet
      Determines what type of neural network is used for additional training. All types of neural networks from the section are supported https://huggingface.co/models?pipeline_tag=image-classification&sort=trending
    It makes sense to leave the value set 'facebook/convnextv2-base-22k-224' which provides the highest accuracy that I have tested or "facebook/convnextv2-tiny-1k-224",  if you are interested in maximum speed with a loss of accuracy of 3-5%.

    test_size = 0.2
    	The program automatically divides each group into two parts: training and testing. In the first part, the neural network is trained, in the second, which the neural network does not see during training, it is checked. The optimal values ​​are usually in the range of 0.2-0.3 and with a small number of images (up to 40) in a group 0.2 is selected, with a large number 0.25 - 0.3.

    batch_size 
    	Determines the size of the simultaneously analyzed group of images to build the index. Depends on the amount of GPU memory and RAM. The minimum value of 16 will allow training on weak hardware, 64 and 128 - for owners of powerful computers with a GPU of 16 GB or more.

    max_equal_distance
    	Defines the maximum distance in the n-dimensional space of the neural network at which images are considered very similar. Used to filter Errors results. It is selected experimentally for each type of neural network. Set by default for 'facebook/convnextv2-base-22k-224'
    ```


2. Start of the program.

    ```
    Go to the working directory and run the command
    	python run.py
    	Open Chrome at localhost:8000 or, if the server is on a remote host, server_address:8000
    ```


3. View the dataset,

    ```
    remove visible errors, for example irrelevant images in groups, expand the dataset using Google Images, if necessary.
    ```


4. Go to tab Learning tab

    ```
     and click Start learning.
    Wait until the end and set the trained network as a system one by clicking button Set trained as the main button.
    ```


5. Analyze errors by clicking Calculate.

    ```
    Correct errors if possible as described above.
    ```


6. If the errors are corrected, go to step 4.

    ```
    Otherwise, go to the Image analysis tab and test the system using images from the Internet.
    ```


<h2>
    		REST - server.</h2>



    CV Tools with a trained neural network supports a REST interface for using by external systems.

1.    Server_address/cv?file_path

        Where file_path is the local path to the file or http address.


        Example:


[http://localhost:8000/cv?/home/george/Projects/save/animals/bison/4a11160cd7.jpg](http://localhost:8000/cv?/home/george/Projects/save/animals/bison/4a11160cd7.jpg)



2.   Server_address/cv?file_path:how_many

        Where file_path is the local path to the file or http address.


        How_many - how many top values ​​to return


        Example:


[http://localhost:8000/cv?/home/george/Projects/save/animals/bison/4a11160cd7.jpg](http://localhost:8000/cv?/home/george/Projects/save/animals/bison/4a11160cd7.jpg):3

	 The returned result in JSON like

	
![image](https://github.com/Claus1/cvtools/assets/1247062/df3c61c4-6efb-495e-98e0-694f5fd7f0de)


An example dataset used in preparing the article:

[https://www.kaggle.com/datasets/iamsouravbanerjee/animal-image-dataset-90-different-animals](https://www.kaggle.com/datasets/iamsouravbanerjee/animal-image-dataset-90-different-animals)

A possible problem:

	The program was tested on Linux and Windows 10 with python 3.10.12. Python  versions for Windows have a bug (in my opinion) in the asyncio library, which does not allow visual just-in-time synchronization of the learning process with the state of CV tools. An adhoc bug fix has been made for version Python 3.10; this non-block problem is possible for other Python versions. 
