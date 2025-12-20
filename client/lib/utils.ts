import { TenantConfig } from "@/types/tenant";

export async function getTenantConfig(tenant: string): Promise<TenantConfig> {
  return Promise.resolve({
    tenant,
    name: tenant,
  });
}