FROM payara/micro

# the Payara Micro Docker image provides a directory 
# from which applications will be deployed on startup
COPY target/build.war $DEPLOY_DIR
