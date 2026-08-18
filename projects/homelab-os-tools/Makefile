.PHONY: up down upload policy fetch status

### Verified against account 690712292635 on us-east-2.
REGION        ?= us-east-2
ACCOUNT_ID    ?= 690712292635
### amzn-ec2-macos-15.7.7-20260514-022421 (x86_64_mac, pairs with mac2.metal).
### For Apple silicon use ami-0d0d03fa19a9d4754 with INSTANCE_TYPE=mac2-m2.metal.
AMI_ID        ?= ami-00e187b3f31f0efbd
### macOS requires a .metal type on a dedicated host. t2.micro is NOT valid.
INSTANCE_TYPE ?= mac2.metal
AVAILABILITY_ZONE ?= us-east-2b
### An existing EC2 key pair name, for SSH debugging if the run misbehaves.
KEY_NAME      ?= minecraft.pub
BUCKET        ?= python-lib-690712292635-us-east-2-an
BUCKET_ARN    ?= arn:aws:s3:::$(BUCKET)
PREFIX        ?= macos-userdata-test
ROLE_NAME     ?= minecraft-admin-role
PROFILE_NAME  ?= minecraft-admin
POLICY_NAME   ?= macos-userdata-test-s3-scoped
TAG           ?= macos-userdata-test
AWS           ?= aws --region $(REGION)

upload:
	@echo "### Syncing project files to s3://$(BUCKET)/$(PREFIX)/ ###"
	@$(AWS) s3 sync . s3://$(BUCKET)/$(PREFIX)/ \
		--exclude "*" \
		--include "src/*" \
		--include "test.py" \
		--include "pyproject.toml" \
		--exclude "*.pyc" \
		--exclude "*__pycache__*" \
		--exclude "*.egg-info/*"
	@echo "### Upload complete ###"

policy:
	@echo "### Applying least-privilege inline policy ###"
	@$(AWS) iam put-role-policy \
		--role-name $(ROLE_NAME) \
		--policy-name $(POLICY_NAME) \
		--policy-document file://iam-policy.json
	@echo "### Policy $(POLICY_NAME) applied to $(ROLE_NAME) ###"

up: upload
	@echo "### Creating IAM role and instance profile... ###"
	@$(AWS) iam create-role --role-name $(ROLE_NAME) \
		--assume-role-policy-document '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"Service":"ec2.amazonaws.com"},"Action":"sts:AssumeRole"}]}' \
		>/dev/null 2>&1 || echo "role exists, continuing"
	@$(MAKE) --no-print-directory policy
	@$(AWS) iam create-instance-profile --instance-profile-name $(PROFILE_NAME) \
		>/dev/null 2>&1 || echo "instance profile exists, continuing"
	@$(AWS) iam add-role-to-instance-profile \
		--instance-profile-name $(PROFILE_NAME) --role-name $(ROLE_NAME) \
		>/dev/null 2>&1 || echo "role already attached, continuing"
	@echo "### Waiting 10s for IAM propagation ###"
	@sleep 10
	@echo "### Allocating dedicated host (macOS requires one) ###"
	@$(AWS) ec2 allocate-hosts \
		--instance-type $(INSTANCE_TYPE) \
		--availability-zone $(AVAILABILITY_ZONE) \
		--auto-placement on \
		--quantity 1 \
		--tag-specifications 'ResourceType=dedicated-host,Tags=[{Key=Project,Value=$(TAG)}]' \
		--query 'HostIds[0]' --output text > host_id.txt
	@echo "host: $$(cat host_id.txt)"
	@echo "### WARNING: dedicated hosts bill for a 24h minimum (Apple licensing) ###"
	@echo "### Launching EC2 instance... ###"
	@$(AWS) ec2 run-instances \
		--image-id $(AMI_ID) \
		--count 1 \
		--instance-type $(INSTANCE_TYPE) \
		--key-name $(KEY_NAME) \
		--placement "HostId=$$(cat host_id.txt),Tenancy=host" \
		--iam-instance-profile Name=$(PROFILE_NAME) \
		--user-data file://user-data.sh \
		--tag-specifications 'ResourceType=instance,Tags=[{Key=Project,Value=$(TAG)}]' \
		--query 'Instances[0].InstanceId' \
		--output text > instance_id.txt
	@echo "### Launched $$(cat instance_id.txt) ###"
	@echo "macOS boots slowly. Results land in ~10-15 min at:"
	@echo "  s3://$(BUCKET)/$(PREFIX)/output/result-latest.txt"
	@echo "Run 'make fetch' to retrieve, then 'make down' to clean up."

status:
	@if [ -f instance_id.txt ]; then \
		$(AWS) ec2 describe-instances --instance-ids $$(cat instance_id.txt) \
			--query 'Reservations[0].Instances[0].State.Name' --output text; \
	else echo "no instance_id.txt"; fi
	@$(AWS) s3 ls s3://$(BUCKET)/$(PREFIX)/output/ || true

fetch:
	@echo "### Fetching latest result ###"
	@$(AWS) s3 cp s3://$(BUCKET)/$(PREFIX)/output/result-latest.txt ./result-latest.txt
	@cat ./result-latest.txt

down:
	@echo "### Terminating AWS instance... ###"
	@if [ -f instance_id.txt ]; then \
		$(AWS) ec2 terminate-instances --instance-ids $$(cat instance_id.txt) >/dev/null 2>&1 || true; \
		$(AWS) ec2 wait instance-terminated --instance-ids $$(cat instance_id.txt) || true; \
		rm -f instance_id.txt; \
	fi
	@echo "### Cleaning up IAM in reverse order... ###"
	@$(AWS) iam remove-role-from-instance-profile \
		--instance-profile-name $(PROFILE_NAME) --role-name $(ROLE_NAME) 2>/dev/null || true
	@$(AWS) iam delete-instance-profile --instance-profile-name $(PROFILE_NAME) 2>/dev/null || true
	@$(AWS) iam delete-role-policy --role-name $(ROLE_NAME) --policy-name $(POLICY_NAME) 2>/dev/null || true
	@$(AWS) iam delete-role --role-name $(ROLE_NAME) 2>/dev/null || true
	@echo "### Releasing dedicated host... ###"
	@if [ -f host_id.txt ]; then \
		$(AWS) ec2 release-hosts --host-ids $$(cat host_id.txt) || \
		echo "NOTE: release failed. Apple licensing blocks release for 24h after allocation."; \
		rm -f host_id.txt; \
	fi
	@echo "### Teardown complete. ###"
