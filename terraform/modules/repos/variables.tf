variable "repos" {
  description = "Map of Git repositories"
  type = map(object({
    url          = string
    git_provider = string
    path         = string
    branch       = optional(string)
    tag          = optional(string)
  }))
  default = {}
}
