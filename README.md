# AI Travel Agent

## Implementing an AI Travel Agent using OpenAI's text API and LangChain framework to track information about future events with the help of duckduckgo search engine, wikipedia and other websites.

### Setting up AWS Cloud with a Docker Image, Step by Step:

<details>
  <summary>1. Create a `requirements.txt` file:</summary>
  
  - 1.1. Make sure to create a `requirements.txt` file containing all the python packages you used in the project.

</details>


<details>
  <summary>2. Create a image of your project with Docker:</summary>

  - 2.1. Install Docker Desktop;
  - 2.2. Create the Dockerfile;
  - 2.3. Build the image:
    ``` python
    docker build --platform linux/x86_64 -t agent .

</details>


<details>
  <summary>3. Setting up AWS ECR Repository:</summary>

  - 3.1. Login at [AWS Website](https://aws.amazon.com/);
  - 3.2. Create a Private Repository at [Amazon Elastic Container Registry (ECR)](https://us-east-2.console.aws.amazon.com/ecr/private-registry/repositories?region=us-east-2) with the name `travelagent`, for example.

</details>


<details>
  <summary>4. Setting up AWS CLI:</summary>

  - 4.1. Install [AWS Command Line Interface (CLI)](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html), copying the commands to your terminal, according to your Operational System;
  - 4.2. Verify installation with the following commands:
    ```
    which aws
    aws --version
  - 4.3. AWS Configure: requires AWS Access Key ID and AWS Secret Access Key.
    - To find those keys, go to [AWS Identity and Access Management (IAM)](https://us-east-1.console.aws.amazon.com/iam/home?region=us-east-2#/home);
    - Then, find Users > your_user > Security credentials;
    - Create an Access Key, then copy paste your keys in the terminal, after typing the following command:
      ```
      aws configure
    - Lastly, confirm your region at AWS Home Console, next to your username, at the top right corner.
    
</details>


<details>
  <summary>5. Push your API Image to your AWS ECR Repository via AWS CLI:</summary>
  
  - 5.1. Head to the ECR Repository > View Push Commands.
      - Copy and paste the push commands into your terminal.
      - At this point, make sure to build, tag and push everytime there's a change to the code. Also, don't forget to deploy the new image to the Lambda function.

  
</details>


<details>
  <summary>6. Create Lambda Function:</summary>
  
  - 6.1. Inside AWS Panel, search for [Lambda](https://us-east-2.console.aws.amazon.com/lambda/home?region=us-east-2#/discover);
  - 6.2. Create a new function with a Container image:
      - Browse for the ECR Repository Image;
      - Select Architecture x86_64.
  - 6.3. Edit function's configuration:
      - Increase Memory to 512 MB;
      - Increase timeout (e.g. 10 minutes).  
  - 6.4. Insert Environment Variable:
      - Inside the Lambda Function, go to Configuration > Environment variables;
      - fill the 'Key' field with `OPENAI_API_KEY` and the 'Value' field with the actual API Key.
  
</details>


<details>
  <summary>7. Create Lambda Test:</summary>

  - 7.1. Inside the Lambda function, go to Test:
      - Insert an Event name;
      - In this example, create a 'question' tag in the JSON Event with an example of an actual user prompt;
      - Save and Run the Test;
      - Check for execution status and details and see if corresponds to what's expected.
    
</details>


<details>
  <summary>8. Exposing the application to the internet via AWS EC2 Load Balancers:</summary>
  
  - 8.1. Inside AWS Panel, search for [Elastic Compute Cloud (EC2)](https://us-east-2.console.aws.amazon.com/ec2/home?region=us-east-2#Home);
  - 8.2. At the left side Panel, look for Load Balancing > Load Balancers > Create Load Balancer > Application Load Balancer:
    - Scheme: Internet-facing;
    - Load balancer IP address type: IPv4;
    - Select the existing VPC and all Subnets;
    - Security groups: Default;
    - Protocol: HTTP, Port: 80, Create target group.
  - 8.3. Creating a target group:
    - Target type: Lambda Function;
    - Provide a Target group name (e.g. target-travelagent);
    - Select the recently created Lambda Function, with Version set to `$LATEST`
  - 8.4. Create Load Balancer (after adding the target group);
  - 8.5. Edit Security configuration:
      - Head to Security > Open security group ID > Edit inbound rules:
          - Type: HTTP;
          - Port: 80;
          - Source: Custom -> `0.0.0.0/0`.
  - 8.6. Make sure to copy the DNS Name from the Load Balancer to call the API.
    
</details>

## Results: Creating a call to the API.

#### `try.curl` file provides an example of a call to the API using curl. Here's the code:
```curl
  curl -X POST "http://api-travelagent-232686593.us-east-2.elb.amazonaws.com" \
  -H "Content-Type: application/json" \
  -d '{
      "question": "Vou viajar para Londres em agosto de 2024. Quero que faça um roteiro de viagem para mim com eventos que irão ocorrer na data da viagem e com o preço da passagem de São Paulo para Londres ida e volta em reais."
  }'
  ```
> The output should be printed in your terminal.


<sub>This project is part of the AI track at the 16th edition of the [Next Level Week (NLW Journey)](https://www.rocketseat.com.br/eventos/nlw)  held by [Rocketseat](https://www.rocketseat.com.br/discover) from 8-11 of July/2024.</sub>
