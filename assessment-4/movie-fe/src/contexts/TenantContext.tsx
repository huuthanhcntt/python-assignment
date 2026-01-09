import { createContext, useContext, useEffect, useState } from 'react';
import type { ReactNode } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { moviesApi } from '../api/movies';

interface TenantContextType {
  tenant: string;
  availableTenants: string[];
  isLoading: boolean;
}

const TenantContext = createContext<TenantContextType | undefined>(undefined);

const DEFAULT_TENANT = 'trending';

// Module-level cache to prevent duplicate API calls
let tenantsCache: string[] | null = null;
let tenantsFetchPromise: Promise<string[]> | null = null;

const fetchTenants = async (): Promise<string[]> => {
  // Return cached tenants if available
  if (tenantsCache !== null) {
    return tenantsCache;
  }

  // Return existing promise if already fetching
  if (tenantsFetchPromise !== null) {
    return tenantsFetchPromise;
  }

  // Create new fetch promise
  tenantsFetchPromise = moviesApi
    .getTenants()
    .then((tenants) => {
      tenantsCache = tenants;
      tenantsFetchPromise = null;
      return tenants;
    })
    .catch((error) => {
      console.error('Error fetching tenants:', error);
      tenantsCache = [DEFAULT_TENANT];
      tenantsFetchPromise = null;
      return [DEFAULT_TENANT];
    });

  return tenantsFetchPromise;
};

export function TenantProvider({ children }: { children: ReactNode }) {
  const { tenant: urlTenant } = useParams<{ tenant: string }>();
  const navigate = useNavigate();
  const [availableTenants, setAvailableTenants] = useState<string[]>(tenantsCache || []);
  const [isLoading, setIsLoading] = useState(tenantsCache === null);

  // Convert URL-friendly slug (top-rated) to API tenant (top_rated)
  const tenant = urlTenant?.replace(/-/g, '_');
  const currentTenant = tenant || DEFAULT_TENANT;

  // Fetch available tenants from API (with caching)
  useEffect(() => {
    let isMounted = true;

    const loadTenants = async () => {
      const tenants = await fetchTenants();
      if (isMounted) {
        setAvailableTenants(tenants);
        setIsLoading(false);
      }
    };

    loadTenants();

    return () => {
      isMounted = false;
    };
  }, []);

  // Validate tenant and redirect if invalid
  useEffect(() => {
    if (isLoading || availableTenants.length === 0) {
      return;
    }

    // Convert tenant to URL-friendly slug for redirects
    const tenantToUrlSlug = (t: string) => t.replace(/_/g, '-');

    // If no tenant in URL, redirect to default
    if (!tenant && window.location.pathname === '/') {
      navigate(`/${tenantToUrlSlug(DEFAULT_TENANT)}`, { replace: true });
      return;
    }

    // If tenant is not in the available list, redirect to default
    if (tenant && !availableTenants.includes(tenant)) {
      console.warn(`Tenant "${tenant}" not found. Redirecting to ${DEFAULT_TENANT}`);
      navigate(`/${tenantToUrlSlug(DEFAULT_TENANT)}`, { replace: true });
      return;
    }

    // Store valid tenant in localStorage for API client interceptor
    if (tenant) {
      localStorage.setItem('tenant', tenant);
    }
  }, [tenant, availableTenants, isLoading, navigate]);

  return (
    <TenantContext.Provider value={{ tenant: currentTenant, availableTenants, isLoading }}>
      {children}
    </TenantContext.Provider>
  );
}

export function useTenant() {
  const context = useContext(TenantContext);
  if (context === undefined) {
    throw new Error('useTenant must be used within a TenantProvider');
  }
  return context;
}
