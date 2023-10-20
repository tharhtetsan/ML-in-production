### Terraform commands

Temporarly remove pre-commit hook
```bash
rm -rf .git/hooks
```

```bash
terraform init
terraform plan
terraform apply
```

### Run with variable
```bash
terraform init

terraform plan -var-file=vars/stg.tfvars

terraform apply -var-file=vars/stg.tfvars

terraform destroy -var-file=vars/stg.tfvars
```
