#!/bin/bash

PROJECT_NAME=ytmp3-telegram-bot
ENV_FILE=.env

MODE=$1
ACTION=$2

# Define valid modes and actions
VALID_MODES=("prod" "dev")
VALID_ACTIONS=("up" "down")

# Check for valid mode
if [[ ! " ${VALID_MODES[@]} " =~ " ${MODE} " ]]; then
    echo "Usage: $0 {prod|dev} {up|down}"
    exit 1
fi

# Check for valid action
if [[ ! " ${VALID_ACTIONS[@]} " =~ " ${ACTION} " ]]; then
    echo "Usage: $0 {prod|dev} {up|down}"
    exit 1
fi

# Set the correct Compose file based on mode
COMPOSE_FILE="compose.${MODE}.yml"

# Start or stop based on action
if [ "$ACTION" == "up" ]; then
    echo "Starting in $MODE mode..."
    if [ "$MODE" == "prod" ]; then
        docker compose -f $COMPOSE_FILE --env-file $ENV_FILE -p $PROJECT_NAME up --build --remove-orphans -d
    else
        docker compose -f $COMPOSE_FILE --env-file $ENV_FILE -p $PROJECT_NAME up --build --remove-orphans
    fi
elif [ "$ACTION" == "down" ]; then
    echo "Stopping in $MODE mode..."
    docker compose -f $COMPOSE_FILE --env-file $ENV_FILE -p $PROJECT_NAME down
fi
