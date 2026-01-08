# Secrets Module

terraform {
  required_providers {
    databricks = {
      source = "databricks/databricks"
    }
  }
}

# Secret Scopes
resource "databricks_secret_scope" "scopes" {
  for_each = var.secret_scopes

  name = each.value.name

  # Databricks-managed or Azure Key Vault
  dynamic "keyvault_metadata" {
    for_each = lookup(each.value, "keyvault_metadata", null) != null ? [each.value.keyvault_metadata] : []
    content {
      resource_id = keyvault_metadata.value.resource_id
      dns_name    = keyvault_metadata.value.dns_name
    }
  }
}

# Secrets
resource "databricks_secret" "secrets" {
  for_each = var.secrets

  scope        = databricks_secret_scope.scopes[each.value.scope_key].name
  key          = each.value.key
  string_value = each.value.string_value
}

# Secret ACLs
resource "databricks_secret_acl" "acls" {
  for_each = var.secret_acls

  scope      = databricks_secret_scope.scopes[each.value.scope_key].name
  principal  = each.value.principal
  permission = each.value.permission # READ, WRITE, MANAGE
}
