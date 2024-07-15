# AI Travel Agent

## Implementing an AI Travel Agent using OpenAI's text API and LangChain framework to track information about future events with the help of duckduckgo search engine, wikipedia and other websites.

#### This project is part of the AI track at the 16th edition of the 'Next Level Week' (NLW Journey) held by Rocketseat from 8-11 of July/2024. Further information can be found at their [website.](https://www.rocketseat.com.br/eventos/nlw)


### Setting up AWS Cloud with a Docker Image, Step by Step:

<details>
  <summary>1. Create a `requirements.txt` file</summary>
  
  - Make sure to create a `requirements.txt` file containing all the python packages you used in the project.

  
</details>

<details>
  <summary>2. Create a image of your project with Docker:</summary>


  - Install Docker Desktop;
  - Create the Dockerfile;
  - Build the image:
    ``` python
    docker build --platform linux/x86_64 -t agent .

  
</details>

<details>
  <summary>3. Setting up AWS ECR Repository:</summary>

  - Login at [AWS Website](https://aws.amazon.com/);
  - Create a Private Repository at [Amazon Elastic Container Registry (ECR)](https://us-east-2.console.aws.amazon.com/ecr/private-registry/repositories?region=us-east-2) with the name `travelagent`, for example.
</details>


<details>
  <summary>4. Setting up AWS CLI:</summary>

  - Install [AWS Command Line Interface (CLI)](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html);
  - Verify installation with the following commands:
    ```
    which aws
    aws --version
  - AWS Configure: requires AWS Access Key ID and AWS Secret Access Key.
    - To find those keys, go to [AWS IAM](https://us-east-1.console.aws.amazon.com/iam/home?region=us-east-2#/home);
    - Then, find Users>your_user>Security credentials;
    - Create an Access Key, then copy paste your keys in the terminal, after typing the following command:
      ```
      aws configure
    - Lastly, confirm your region at AWS Home Console, next to your username, at the top right corner.
</details>


<details>
  <summary>5. Connect to your AWS ECR Repository via AWS CLI</summary>

</details>
