package org.perimeter.keycloak.multitenancy.rest;

import org.keycloak.models.KeycloakSession;
import org.keycloak.services.resources.admin.AdminAuth;
import org.perimeter.keycloak.multitenancy.MultiTenancyProvider;

import javax.ws.rs.*;
import javax.ws.rs.core.Context;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;

@Path("/tenants")
@Consumes(MediaType.APPLICATION_JSON)
@Produces(MediaType.APPLICATION_JSON)
public class TenantResource {

    private final KeycloakSession session;
    private final AdminAuth auth;

    public TenantResource(@Context KeycloakSession session, AdminAuth auth) {
        this.session = session;
        this.auth = auth;
    }

    @POST
    public Response createTenant(TenantRepresentation tenant) {
        // Validate admin permissions
        if (!auth.hasRealmRole("admin")) {
            return Response.status(Response.Status.FORBIDDEN).build();
        }

        try {
            MultiTenancyProvider provider = session.getProvider(MultiTenancyProvider.class);
            provider.createTenant(tenant.getId(), tenant.getName(), tenant.getAdminEmail());
            
            return Response.created(null).build();
        } catch (Exception e) {
            return Response.serverError().entity(e.getMessage()).build();
        }
    }

    @GET
    @Path("/{tenantId}")
    public Response getTenant(@PathParam("tenantId") String tenantId) {
        // Implementation for getting tenant details
        return Response.ok().build();
    }

    @DELETE
    @Path("/{tenantId}")
    public Response deleteTenant(@PathParam("tenantId") String tenantId) {
        // Implementation for deleting a tenant
        return Response.ok().build();
    }

    public static class TenantRepresentation {
        private String id;
        private String name;
        private String adminEmail;

        // Getters and setters
        public String getId() { return id; }
        public void setId(String id) { this.id = id; }
        public String getName() { return name; }
        public void setName(String name) { this.name = name; }
        public String getAdminEmail() { return adminEmail; }
        public void setAdminEmail(String adminEmail) { this.adminEmail = adminEmail; }
    }
}
