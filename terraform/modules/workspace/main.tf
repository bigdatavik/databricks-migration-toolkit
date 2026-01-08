# Workspace Module - Folders and Notebooks

terraform {
  required_providers {
    databricks = {
      source = "databricks/databricks"
    }
  }
}

# Workspace Directories
resource "databricks_directory" "directories" {
  for_each = var.directories

  path = each.value.path
}

# Notebooks
resource "databricks_notebook" "notebooks" {
  for_each = var.notebooks

  path     = each.value.path
  language = lookup(each.value, "language", "PYTHON")
  source   = each.value.source
  
  # Optional: content for inline notebooks
  content_base64 = lookup(each.value, "content_base64", null)
}

# DBFS Files (for libraries, init scripts, etc.)
resource "databricks_dbfs_file" "files" {
  for_each = var.dbfs_files

  path   = each.value.path
  source = each.value.source
}
