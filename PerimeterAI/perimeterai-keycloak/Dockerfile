FROM maven:3.9-eclipse-temurin-17 as builder

WORKDIR /opt/keycloak

# Copy the source code from src directory
COPY src ./src
COPY pom.xml .

# Build Keycloak
RUN mvn clean package -DskipTests -Dmaven.test.skip=true

# Final stage
FROM quay.io/keycloak/keycloak:latest

# Copy the built artifacts from builder
COPY --from=builder /opt/keycloak/target/* /opt/keycloak/
# Copy theme from builder stage (note: theme not themes)
COPY --from=builder /opt/keycloak/src/main/resources/theme/* /opt/keycloak/themes/

WORKDIR /opt/keycloak

EXPOSE 8081
ENTRYPOINT ["/opt/keycloak/bin/kc.sh"]