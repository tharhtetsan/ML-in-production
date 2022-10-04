## Data and model versioning with DVC

##### Installation

```bash
pip install dvc

dvc init
```


Remark : dvc can only start under git directory.

##### Check dvc records are created or not.

```bash
git status
```

##### Commit first commit.

```bash
git commit -m "first dvc"

git push
```



##### Add data to dvc

```bash
dvc add 2_data_and_model_versioning\skin_cancer_dataset\Benign_keratosis-like_lesions\

dvc add 2_data_and_model_versioning\skin_cancer_dataset\Melanocytic_nevi\

dvc add 2_data_and_model_versioning\skin_cancer_dataset\Melanoma\
```

##### Now check the following:

```bash
cat 2_data_and_model_versioning\.gitignore
cat 2_data_and_model_versioning\skin_cancer_dataset\Benign_keratosis-like_lesions.dvc
cat 2_data_and_model_versioning\skin_cancer_dataset\Melanoma.dvc
```



add Remote Storage to dvc
dvc remote add -d storage gdrive://

