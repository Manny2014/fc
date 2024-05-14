output "gke_cluster" {
  description = "GKE Cluster"
  value       = module.gke
  sensitive = true
}