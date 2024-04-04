<!-- README HEADER -->
<br>
<div align="center">
<h2 align="center">MADO Data Lake - Speed Layer</h2>
<h3 align="center">msk-python-gg-events-producer</h3>
<br/>

<!-- BADGES CONFIGURATION -->
[aws]: https://img.shields.io/badge/AWS-000000?style=for-the-badge&logo=amazonaws&logoColor=yellow
[bash]: https://img.shields.io/badge/Bash-000000?style=for-the-badge&logo=linux&logoColor=white
[python]: https://img.shields.io/badge/python-000000?style=for-the-badge&logo=python&logoColor=yellow
[kafka]: https://img.shields.io/badge/kafka-000000?style=for-the-badge&logo=apache-kafka&logoColor=blue
[git]: https://img.shields.io/badge/Gitlab-000000?style=for-the-badge&logo=git&logoColor=orange
[repositoryurl_badge]: https://git-codecommit.us-east-2.amazonaws.com/v1/repos/msk-python-producer-dl.git
[jenkins]: https://img.shields.io/badge/Jenkins-000000?style=for-the-badge&logo=Jenkins&logoColor=red
[joburl_badge]: job_url
[prismacloud]: https://img.shields.io/badge/Prisma-000000?style=for-the-badge&logo=prisma&logoColor=#6adef7
[primacloudurl_badge]: prisma_url



![aws][aws]
![python][python]
![kafka][kafka]


[![git][git]][repositoryurl_badge]

</div>

<!-- INDICE DE CONTENIDOS -->
<details>
  <summary>Contenido</summary>
  <ol>
   <li>
      <a href="#Requisitos">Requerimentos</a>
    </li>
    <li>
      <a href="#about-the-project">Ambientacion</a>
    </li>
    <li>
      <a href="#about-the-project">Diagrama de Arquitectura</a>
    </li>
    <li>
      <a href="##8 - Implementacion">Implementacion</a>
    </li>
    <li>
      <a href="#about-the-project">Directorio de responsables internos</a>
    </li>
  </ol>
</details>

<!-- 
Mejoras:
  Mejorar el Topic Schema para leer de manera mas comoda
  XML En una sola linea
  Base de datos en dynamodb -->


# 1 - Requerimentos

### Python Requirements


* Version de python
* Exposicion de Requerimentos


### Kafka Bus Requirements

* Necesidad de Kafka
* Creacion de Topicos

Exporte la KAFKA_HOME 

```sh
$KAFKA_HOME/bin/kafka-topics.sh \
--create \
--bootstrap-servers localhost:9092 \
--replication-factor 1 \
--partitions 1 \
--topic SPDLAY1
```

### Golden Gate File System Events

* Necesidad de compartir volument de eventos de File System

* Tablas a Monitorear

* Carpeta de FileSystem a monitorear


# 2 - Ambientacion Desarrollo

### Local Kafka Cluster
### Golden Gate Events Mimics

```python
python3 python-golden-gate-oracle-mimics.py
```

### Sync File Handler

# 3 - Diagrama de Arquitectura

Anexo de diagramas de arquitectura los cuales han sido aprobados por el departamento de seguridad informatica y son referencia del aprovisionamiento de recursos y configuraciones que se realizara en la cuenta mediante infraestructura como codigo 

### Dev

<img src="path-to-diagram-data-lake-speed-layer-dev.png" 
alt="Diagrama de Arquitectura Cloud Dev"/>

### Qa

<img src="path-to-diagram-data-lake-speed-layer-qa.png" 
alt="Diagrama de Arquitectura Cloud Qa"/>

### Prod

<img src="path-to-diagram-data-lake-speed-layer-prod.png" 
alt="Diagrama de Arquitectura Cloud Prod"/>

---
---

---
---
# 8 - Implementacion

### Pre requisitos

- [✓] Solicitud de segmentos de red al area [Analisis de Trafico y Operacion de Firewalls](perf_app@aztecaservicios.com)
- [✓] Subneteo y asignacion de ips a arquitectura
- [✓] Solicitud de cuentas AWS al equipo [Cyaal]()
- [✓] Acceso IAM cuenta de consola AWS con permisos de encargado
- [✓] Compartir accesos de consola y programaticos a [DevOps CoE Apis]() para su configuracion el flujo cicd
- [✓] Compra  y configuracion del dominio util para el proyecto
- [✓] Carga de Arquitectura de ecosistema a IEECO

### *Backend*: 

   * Descripcion: recursos necesarios para el despliegue de la infraestructura con terraform y persistir los ultimos estados disponibles de la infraestructura cloud.
   los estados de la infrastructura son remotos al directorio de ejecucion y pueden consultarse a un bucket s3 y tabla de dynamodb para saber cuando existe un despliegue en curso y saber el ultimo estado de la infrastructura aprovisionada. 

   * Recursos:
       * Tabla Dynamodb
       * Bucket s3
   
   * Despliegue: 
       1. Indique los valores para su arquitectura llenando el archivo [Iaac/backend/terraform-backend/tfvars/ambiente.tfvars]() segun el ambiente a desplegar
       2. Indique en el mensaje del commit la palabra reservada _*"backend"*_ para realizar unicamente el despliegue del backend 
       3. Realize el push a la ramas correspondientes al ambiente donde requiere desplegar el backend terraform [dev,qa,prod]()


---
---

# 9 - Directorio de responsables internos y provedores



### Infrastructura Cloud

* [metadata.roles.arquitectoCloud.nombre](metadata.roles.arquitectoCloud.email) - Arquitecto Cloud - Centro de Excelencia Cloud
* [Analisis de Trafico y Operacion de Firewalls](perf_app@aztecaservicios.com) - Carco Paatof 

<br>
<div align="right">
<br>Data Lake Speed Layer
<br>Autores: Arquitectura Data
</div>