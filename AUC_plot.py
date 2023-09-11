import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import glob, math, os, argparse, json

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()   
    parser.add_argument('-in','--inputDir',     type=str, help="Directory where the ml__best/mid/low final trainings are stored.", required=True)
    parser.add_argument('-out','--outputDir',   type=str, help="Directory to store the final plots.", required=False)
    args = parser.parse_args()
    
    inputDir  = args.inputDir
    outputDir = args.outputDir

    keys = ['best','mid','low']
    mass_points = [400,800,1250]

     
    all_folders = [ item for item in os.listdir(inputDir) if os.path.isdir(os.path.join(inputDir,item))]
    ml__folders = []
    json_files  = []
    for folder_name in all_folders:
        for key in keys:
            if key in folder_name:
                ml__folders.append(folder_name)

    for folder in ml__folders:
            inputdir    = os.path.join(inputDir,folder)
            directories = os.listdir(inputdir)
            
            modeldirtemp = [item for item in os.listdir(inputdir) if os.path.isdir(os.path.join(inputdir,item))]
            for model in modeldirtemp:
                modeldir = os.path.join(inputdir,model)

            trainingdirtemp = [item for item in os.listdir(modeldir) if os.path.isdir(os.path.join(modeldir,item))]
            for training in trainingdirtemp:
                trainingdir = os.path.join(modeldir,training)
                aucdirtemp = [item for item in os.listdir(trainingdir) if item.endswith('auc_score.json')]
                for auc_file in aucdirtemp:
                    aucdir = os.path.join(trainingdir,auc_file)
                    #print(aucdir)
                    json_files.append(aucdir)

    auc_dict = {}    
    colours  = ['#380282', '#3f00ff', '#41c5b8', '#380282', '#3f00ff', '#41c5b8', '#380282','#3f00ff','#41c5b8'] 
    counter  = 0 
    labels   = []

    for mass in mass_points:
        
        label = 'm' + str(mass) 
        for key in keys:
            colour=colours[counter]
            counter+=1
            
            auc_values  = 'm' + str(mass) + key
            auc_average = 'm' + str(mass) + key + '_average'
            auc_sigma   = 'm' + str(mass) + key + '_sigma'
            auc_scores  = []
            auc_dict[auc_values] = auc_scores
            for file in json_files:
                if auc_values in file:
                    with open(file) as json_file:
                        json_text = json.load(json_file)
                        auc_score = json_text['auc_score']
                        auc_scores.append(auc_score[0])

            average = np.mean(auc_scores)
            sigma = np.std(auc_scores)
            auc_dict.update({auc_values:auc_scores})
            auc_dict.update({auc_average:average})
            auc_dict.update({auc_sigma:sigma})           
            plt.errorbar(mass,average, sigma, fmt='o', markersize=8, capsize=10, color=colour)
        
        labels.append(label)

    #print(auc_dict)

    plt.xticks(ticks=mass_points, labels=labels)
    plt.xlabel('mass point')
    plt.ylabel('AUC Scores')
    plt.title('AUC scores comparison')
    plt.savefig('auc_scores.png')