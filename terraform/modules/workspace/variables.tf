variable "directories" {
  description = "Map of workspace directories to create"
  type = map(object({
    path = string
  }))
  default = {}
}

variable "notebooks" {
  description = "Map of notebooks to create"
  type = map(object({
    path           = string
    source         = string
    language       = optional(string)
    content_base64 = optional(string)
  }))
  default = {}
}

variable "dbfs_files" {
  description = "Map of DBFS files to upload"
  type = map(object({
    path   = string
    source = string
  }))
  default = {}
}
