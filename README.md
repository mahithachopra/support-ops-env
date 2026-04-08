# SupportOpsEnv

## Overview
A real-world customer support simulation environment for training AI agents.

## Motivation
Customer support automation is widely used in industry (Zendesk, Freshdesk). This environment simulates realistic ticket handling workflows.

## Tasks
- Easy: Classification of ticket category
- Medium: Decision of correct action
- Hard: Full resolution of ticket

## Action Space
- classify
- refund
- escalate
- resolve

## Observation Space
- current_ticket (text, category, priority)
- history of actions

## Reward Design
- Partial rewards for correct classification and actions
- Additional reward for resolution
- Penalizes incorrect decisions

## Baseline Results
Final Score: 3.25  
Classification: 1.0  
Action: 1.0  
Resolution: 1.0  

## Run Locally
```bash
pip install -r requirements.txt
python baseline.py