# Git Repos Module

terraform {
  required_providers {
    databricks = {
      source = "databricks/databricks"
    }
  }
}

# Git Repositories
resource "databricks_repo" "repos" {
  for_each = var.repos

  url          = each.value.url
  git_provider = each.value.git_provider # github, gitlab, bitbucket, azureDevOps
  path         = each.value.path

  # Optional: specific branch or tag
  branch = lookup(each.value, "branch", null)
  tag    = lookup(each.value, "tag", null)
}
