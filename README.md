# Cybriant Application to be hosted on Google Cloud Run
    React is extremely compatible with Google Cloud and since we 
    are dealing with containerized applications, taking a modular
    approach to building the application could prove more useful

1) build the react app, then create the docker file 
    you can test if your react app is ready for production by typing npm run build in your VScode terminal

    Step 1: Use an official Node.js runtime as a parent image
    FROM node:16-slim

    Step 2: Set the working directory
    WORKDIR /usr/src/app

    Step 3: Copy package.json and package-lock.json
    COPY package*.json ./

    Step 4: Install app dependencies
    RUN npm install

    Step 5: Copy the current directory contents into the container
    COPY . .

    Step 6: Build the React app for production
    RUN npm run build

    Step 7: Install `serve` to serve the static files
    RUN npm install -g serve

    Step 8: Use serve to serve the build folder
    CMD ["serve", "-s", "build"]

    Step 9: Expose the port the app runs on
    EXPOSE 3000
2) build and then push the docker image to google cloud container
    build the docker image: docker build -t gcr.io/your-project-id/react-app .

    push the docker image: docker push gcr.io/your-project-id/react-app

3) deploy to cloud run (cloud will now gift a url for the app)
    In the google CLI, use the command:
    gcloud run deploy react-app \
    --image gcr.io/your-project-id/react-app \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated

4) Follow the prompts to complete the unification
    select this project and service
    you should have the url at this point and you can test it

5) Set Up Continuous Deployment
    We can link the project to our Git once its already configured
    thus updating our cloud build substantially simpler    

The end result will be our React Application deployed on Google Cloud Run as 
a serverless container.


The tools used are:
React + Vite, Google Cloud Run

I will upload the full guide soon!

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react/README.md) uses [Babel](https://babeljs.io/) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh
