# Odoo

[![Build Status](https://runbot.odoo.com/runbot/badge/flat/1/master.svg)](https://runbot.odoo.com/runbot)
[![Tech Doc](https://img.shields.io/badge/master-docs-875A7B.svg?style=flat&colorA=8F8F8F)](https://www.odoo.com/documentation/master)
[![Help](https://img.shields.io/badge/master-help-875A7B.svg?style=flat&colorA=8F8F8F)](https://www.odoo.com/forum/help-1)
[![Nightly Builds](https://img.shields.io/badge/master-nightly-875A7B.svg?style=flat&colorA=8F8F8F)](https://nightly.odoo.com/)

Odoo is a suite of web based open source business apps.

The main Odoo Apps include an [Open Source CRM](https://www.odoo.com/page/crm),
[Website Builder](https://www.odoo.com/app/website),
[eCommerce](https://www.odoo.com/app/ecommerce),
[Warehouse Management](https://www.odoo.com/app/inventory),
[Project Management](https://www.odoo.com/app/project),
[Billing &amp; Accounting](https://www.odoo.com/app/accounting),
[Point of Sale](https://www.odoo.com/app/point-of-sale-shop),
[Human Resources](https://www.odoo.com/app/employees),
[Marketing](https://www.odoo.com/app/social-marketing),
[Manufacturing](https://www.odoo.com/app/manufacturing),
[...](https://www.odoo.com/)

Odoo Apps can be used as stand-alone applications, but they also integrate seamlessly so you get
a full-featured [Open Source ERP](https://www.odoo.com) when you install several Apps.

## Getting started with Odoo

For a standard installation please follow the [Setup instructions](https://www.odoo.com/documentation/master/administration/install/install.html)
from the documentation.

To learn the software, we recommend the [Odoo eLearning](https://www.odoo.com/slides),
or [Scale-up, the business game](https://www.odoo.com/page/scale-up-business-game).
Developers can start with [the developer tutorials](https://www.odoo.com/documentation/master/developer/howtos.html).

## Security

If you believe you have found a security issue, check our [Responsible Disclosure page](https://www.odoo.com/security-report)
for details and get in touch with us via email.
--------------------------------------------------------------------
docker command:

docker compose up -d
---------------------------------------------------------------------
docker-compose up -d --build 
Nếu bạn có thay đổi trong Dockerfile hoặc các tệp mà Dockerfile sử dụng, 
bạn nên thêm cờ --build để buộc Docker Compose build lại image trước khi 
khởi động container.
---------------------------------------------------------------------
＊Install module.
docker compose exec web python3 odoo-bin -c /etc/odoo/odoo.conf -i {moduleName} -d {dbName} --db_host=db --db_user=odoo --db_password=myodoo --stop-after-init

＊Update module.
docker compose exec web python3 odoo-bin -c /etc/odoo/odoo.conf -u {moduleName} -d {dbName} --db_host=db --db_user=odoo --db_password=myodoo --stop-after-init
  Ex:
    docker compose exec web python3 odoo-bin -c /etc/odoo/odoo.conf -u custom_obic_sale_order -d dbm_hankan --db_host=db --db_user=odoo --db_password=myodoo --stop-after-init

＊Delete module.
docker compose exec web python3 odoo-bin -c /etc/odoo/odoo.conf -d {moduleName} -d {dbName} --db_host=db --db_user=odoo --db_password=myodoo --stop-after-init
---------------------------------------------------------------------
＊Reset app (Mỗi lần cần upgrade reset lại app)
docker compose restart web
---------------------------------------------------------------------
＊View Log.
docker compose logs -f web