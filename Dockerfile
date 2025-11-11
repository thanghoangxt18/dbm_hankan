FROM odoo:18.0

# Switch to root to copy files and set permissions
USER root

# Copy your local source code to container
COPY . /usr/src/odoo

# Create necessary directories and set proper permissions
RUN mkdir -p /usr/src/odoo/addons /var/lib/odoo /var/log/odoo \
    && chown -R odoo:odoo /usr/src/odoo /var/lib/odoo /var/log/odoo \
    && chmod 755 /var/log/odoo

# Switch back to odoo user for security
USER odoo

# Set working directory
WORKDIR /usr/src/odoo

# Expose Odoo port
EXPOSE 8069

# Default command (will be overridden by docker-compose)
CMD ["python3", "odoo-bin"]

#Run this when change core odoo.
#docker exec -it --user root 01_hankan-web-1 bash -c "rm -rf /usr/lib/python3/dist-packages/odoo/addons && cp -rf /usr/src/odoo/addons /usr/lib/python3/dist-packages/odoo/addons && echo '✓ Done!'"