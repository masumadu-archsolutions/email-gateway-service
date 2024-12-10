#!/bin/bash

# Define the directory mappings as an associative array
declare -A dir_mapping
dir_mapping["api/api_v1/endpoints"]=100
dir_mapping["controllers/v1"]=80
dir_mapping["models"]=90

# Directories to check
check_dirs=("api/api_v1/endpoints" "controllers/v1" "models")

for dir in "${check_dirs[@]}"; do
  # Get the corresponding integer value from the mapping
  int_value="${dir_mapping[$dir]}"

  # Get absolute path
  dir_abs_path="$(pwd)/app/$dir"

  # Loop through files in directory
  for file in "$dir_abs_path"/*; do
    if [[ "$file" == *.py ]]; then
      if ! poetry run coverage report --fail-under=$int_value "$file"; then
        echo "Failed for file: $file under coverage: $int_value"
        exit 1
      fi
    fi
  done
done
