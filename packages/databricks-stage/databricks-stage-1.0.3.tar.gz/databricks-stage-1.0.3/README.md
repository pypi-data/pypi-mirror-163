# Overview

This package is meant to be run as a job on a Databricks cluster.  It performs high-speed data export to the specified blob storage location.

The entrypoint in your Databricks job should be `databricks_stage:run`.
