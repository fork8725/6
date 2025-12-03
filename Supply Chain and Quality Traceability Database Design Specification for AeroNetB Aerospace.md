# Supply Chain and Quality Traceability Database

# Design Specification for AeroNetB Aerospace

# I. Title Page

Student Name: [Please Fill in Name]

Student ID: [Please Fill in ID]

Course Name: [Please Fill in Course Name]

Submission Date: [Please Fill in Submission Date]

# II. Project Background and Core Value

## 2.1 Deepening of Business Pain Points

AeroNetB Aerospace is a professional manufacturer of key components for commercial aircraft, with core products covering high-precision aerospace structural parts such as fuselage sections and wing assemblies. To support its global business layout, the company has built a large-scale global supply chain system, with a cooperative network including hundreds of professional parts suppliers. These suppliers provide various supporting aviation parts to the company, and all parts must strictly comply with detailed specification standards and strict certification requirements to meet the extreme pursuit of safety and reliability in the aviation industry. Relying on its professional manufacturing capabilities, the company serves aircraft manufacturers and related aviation enterprises worldwide, providing key component support that meets industry standards.

In the current business operation, AeroNetB Aerospace is facing severe data management bottlenecks: the existing data processing completely relies on fragmented tools, including outdated databases, various spreadsheets, and manually maintained logs. This decentralized management model has caused a series of problems, not only leading to low work efficiency and frequent data duplication, but more critically, resulting in the lack of real-time visibility of business data. This makes it difficult to accurately control key links such as supply chain collaboration and production schedule management, seriously affecting the company's market competitiveness. For example, in the process of coordinating the parts delivery from global suppliers and the connection between the production of fuselage and wing assemblies, due to the inability to obtain real-time key data such as parts inventory and supplier production progress, problems such as delayed production plan adjustments, inventory overstocking or shortages often occur. At the same time, the specification parameters and certification information of parts are stored in different tools, making query and traceability difficult, which not only increases the risk of quality control, but also reduces the response speed to changes in customer needs. Behind these problems lies an urgent need for multi-type data integration, real-time data processing and secure data access.

## 2.2 Database Construction Objectives

1. Traceability Efficiency Improvement: Establish a full-link traceability mechanism covering "raw materials - processing - inspection - delivery", reducing the single product traceability time from 4 hours to within 10 minutes.

2. Supply Chain Collaboration Optimization: Realize real-time synchronization of core supplier data, increasing the supplier delivery on-time rate to more than 98.5%.

3. Quality Cost Reduction: Through advanced quality risk early warning, reduce the rework rate of quality problems related to raw materials by 60% and cut quality costs by 30%.

4. Compliance Capability Enhancement: Meet regulatory requirements such as FAA Part 21 and EASA CS-25, achieving a 100% pass rate for traceability data audits.

# III. Requirement Analysis and Technical Specifications

**3.1 Core Business Requirements**

<table border="1" ><tr>
<td>Requirement<br>Category</td>
<td>Specific Requirement Description</td>
<td>Priority</td>
<td>Data Interaction<br>Frequency</td>
</tr><tr>
<td>Supplier Data<br>Management</td>
<td>Management of core<br>supplier qualification<br>information; real-time synchronization of<br>supplier delivery data;quantitative<br>evaluation of supplier quality performance;automatic<br>determination of<br>supplier risk levels</td>
<td>PO</td>
<td>1 time per delivery<br>batch</td>
</tr><tr>
<td>Full-Link Traceability Management</td>
<td>Realize the binding of raw materials and<br>finished products<br>based on unique<br>traceability codes;<br>support forward (raw<br>materials→ finished<br>products) and reverse (finished products →<br>raw materials)<br>traceability;<br>traceability data<br>includes all elements such as equipment,<br>personnel, and<br>parameters</td>
<td>PO</td>
<td>1 time per<br>production link</td>
</tr><tr>
<td>Quality Risk Early<br>Warning</td>
<td>Real-timme analysis of incoming raw material inspection data; early warning of<br>abnormalities in<br>production process<br>quality data; quality<br>risk prediction based<br>on historical data;<br>automatic push of<br>early warning<br>information to<br>relevant responsible<br>persons</td>
<td>PO</td>
<td>1 time per<br>inspection event</td>
</tr><tr>
<td>Supply Chain<br>Collaboration<br>Planning</td>
<td>Associate sales<br>orders with<br>procurement plans;<br>automatically adjust<br>procurement needs<br>based on production<br>progress; analysis of supplier capacity and delivery capability<br>matching; supply<br>chain bottleneck early warning</td>
<td>P1</td>
<td>1 time per day</td>
</tr><tr>
<td>Compliance Report<br>Generation</td>
<td>Automatically<br>generate FAA/EASA<br>compliant traceability reports; support multi-dimensional query<br>and export of<br>traceability data;<br>automatic recording and retention of audit logs;custom<br>configuration of report templates</td>
<td>PO</td>
<td>1 time per audit<br>requirement</td>
</tr></table>

## 3.2 Technical Specification Requirements

### 3.2.1 Performance Specifications

·Traceability code query response time ≤ 500ms, complex full-link traceability query ≤ 3s

·Support simultaneous data access by 100 suppliers, with single-batch data synchronization delay≤30s

·Annual database data increment is approximately 12TB, including 3TB of structured data and 9TB of unstructured data (inspection reports, qualification documents)

·Concurrency support: more than 200 terminals in procurement and quality departments operate simultaneously, and more than 10 compliance reports are generated in parallel

### 3.2.2 Security and Reliability Specifications

·Supplier sensitive data (such as prices, production capacity) is encrypted using the national secret SM4 algorithm, and TLS 1.3 protocol is adopted for transmission

·Database system availability ≥ 99.99%, data backup adopts the"real-time synchronization

+ remote three copies" strategy, with RTO ≤ 15 minutes and RPO ≤ 1 second

·Support traceability data entry in offline environment, with automatic incremental synchronization after network recovery to ensure the integrity of the traceability chain

·Traceability data and audit logs are retained for ≥ 15 years to meet the full-life-cycle traceability requirements of aviation components

# IV. Conceptual Data Model Design

## 4.1 Core Entity Identification

Based on the core requirements of supply chain - quality traceability, 32 core entities are extracted. Key entities include: SupplierQualificationArchive, RawMaterialTraceRecord, BatchTraceRelation, QualityInspectionData, QualityRiskWarning, SupplyChainCollabPlan, etc. The entity relationships cover the full link of "supplier - raw material - production -inspection- delivery-after-sales".

## 4.2 Key Entity Attribute Definition

1. SupplierQualificationArchive - QualificationID (PK), SupplierID (FK), QualificationType (e.g., AS9100D certification), CertificateNumber, IssuingAuthority, EffectiveDate, ExpirationDate, QualificationStatus, AnnuallnspectionRecord, QualificationFileStoragePath, UpdaterID (FK), UpdateTime, DataStatus

2. RawMaterialTraceRecord - TracelD (PK), RawMaterialBatchNo, TraceCode (Unique), SupplierID (FK), PurchaseOrderID (FK), IncomingInspectionID (FK), ReceivingTime, StorageLocation, UsageRecord (Associated with ProductionWorkOrderIDD), RemainingQuantity, ConsumptionCompletionTime, TraceStatus

3.

BatchTraceRelation - RelationID (PK), FinishedProductBatchNo, FinishedProductTraceCode, RawMaterialTraceCode (FK), ProcessingEquipmentID (FK), ProcessParameterSchemelD (FK), InspectorlD (FK), InspectionTime, AssociatedStage (e.g., milling/drilling/assembly), DataSource, RelationStatus

4. QualityRiskWarning - WarningID (PK), WarningObject (RawMaterial/Semi-FinishedProduct/FinishedProduct), ObjectID (FK), RiskType (e.g., composition deviation/dimension out-of-tolerance), RiskLevel (Level 1-5), WarningTriggerCondition, WarningTriggerTime, HandlerID (FK), HandlingStatus, HandlingResult, ClosureTime

## 4.3 Core Entity Relationships

ER diagrams are used to clarify entity association rules, and key relationships are as follows:

·Supplier and Raw Material: One-to-Many (1:N), one supplier can provide multiple batches of raw materials, recording the corresponding relationship between suppliers and raw materials

·Raw Material and Finished Product: Many-to-Many (M:N), associated through

"BatchTraceRelation" to support traceability scenarios where multiple raw materials form a single finished product

·QualityInspectionData and QualityRiskWarning: One-to-Many (1:N), triggering corresponding levels of risk warnings based on inspection data thresholds

·Sales Order and SupplyChainCollabPlan: One-to-Many (1:N), generating corresponding procurement and production collaboration plans based on sales order requirements

·Batch TraceRelation and Equipment: One-to-Many (1:N), the traceability record of one production stage is associated with the operation data of one piece of equipment

<!-- - - U B y P R -- - - - - - - R X d B 0 etg ed - R - - - - he L p wdg B y ee บ/e R - - he - - N 0 e Bs d peed - R Ψ d N -g 8 -pu Buus 4 B / Buues - 0 B 0 Bs - B 3 ต Bg - B THT Beg - - - B su sg - - Bs - - นรนกว - 0 pp PNp B Ay Apu - B ( ep ) pe puooe Se pay ad p pad 1 - Be - - - gg - - Ba - - 0 d R Bue AnT B 0 ค S R Jqn -- 3 ep 100014 B q Seag 0 - - - - - A % B - - V Bng - - B . 0 S - - 大 y P npodp B 0 lee - - m ( ed 1 0apD aes - 0 B dons 8 - sD 1 S NLpg - g -0 - - 0 p Bang 0 S - -->

# V. Logical Data Model Design

## 5.1 Database Architecture Design

A four-layer architecture of "relational database + time-series database + file storage + graph database" is adopted to meet the needs of multi-type data processing and traceability link query:

<table border="1" ><tr>
<td>Architecture Layer</td>
<td>Database Selection</td>
<td>Stored Content</td>
<td>Core Advantages</td>
</tr><tr>
<td>Core Business<br>Layer</td>
<td>PostgreSQL 16</td>
<td>Structured data such as supplier archives, traceability<br>associations, quality warnings,and<br>collaboration plans</td>
<td>Supports complex<br>transactions and<br>associated queries, suitable for storing<br>multi-entity<br>relationship data</td>
</tr><tr>
<td>Time-Series Data<br>Layer</td>
<td>InfluxDB 3.0</td>
<td>Production process<br>quality inspection<br>time-series data,<br>supplier delivery<br>time-series data</td>
<td>High compression<br>ratio, supporting fast aggregate analysis<br>by time window</td>
</tr><tr>
<td>File Storage Layer</td>
<td>MinlO</td>
<td>Unstructured data<br>such as supplier<br>qualification<br>documents,<br>inspection report<br>scans, and process<br>drawings</td>
<td>Supports distributed storage, facilitating<br>association with<br>structured data</td>
</tr><tr>
<td>Traceability Link<br>Layer</td>
<td>Neo4j</td>
<td>Full-link traceability<br>relationship data<br>between raw<br>materials and<br>finished products</td>
<td>Graph structure<br>storage, supporting<br>millisecond-level<br>full-link traceability<br>queries</td>
</tr></table>

## 5.2 Core Table Structure Design

### 5.2.1 Raw Material Trace Record Table

# (rawmaterialtracerecord)

<table border="1" ><tr>
<td>Field<br>Name</td>
<td>Data<br>Type</td>
<td>Constraint<br>Conditions</td>
<td>Default<br>Value</td>
<td>Remark Description</td>
</tr><tr>
<td>traceid</td>
<td>VARC<br>HAR(3 2)</td>
<td>PK, NOT NULL, UNIQUE</td>
<td>-</td>
<td>Traceability ID, format "RMT-<br>YYYYMMDD-XXXXXX"</td>
</tr><tr>
<td>materialb atchno</td>
<td>VARC<br>HAR(2 0)</td>
<td>NOT NULL</td>
<td>-</td>
<td>Raw material batch number,<br>provided by supplier</td>
</tr><tr>
<td>tracecode</td>
<td>VARC<br>HAR(3 6)</td>
<td>NOT NULL,<br>UNIQUE</td>
<td>-</td>
<td>Unique traceability code,<br>generated using UUID</td>
</tr><tr>
<td>supplierid</td>
<td>VARC<br>HAR(2 0)</td>
<td>FK(supplier.suppl ierid), NOT<br>NULL</td>
<td>-</td>
<td>Associated supplier ID</td>
</tr><tr>
<td>purchase<br>orderid</td>
<td>VARC<br>HAR(2 0)</td>
<td>FK(purchaseord er.poid), NOT<br>NULL</td>
<td>-</td>
<td>Associated purchase order ID</td>
</tr><tr>
<td>incomingi nspection<br>id</td>
<td>VARC<br>HAR(3 2)</td>
<td>FK(qualityinspe ction.inspectioni d), NOT NULL</td>
<td>-</td>
<td>Associated incoming<br>inspection ID</td>
</tr><tr>
<td>receiveti me</td>
<td>TIMES TAMP</td>
<td>NOT NULL</td>
<td>CURRENT TIMESTA MP</td>
<td>Raw material receiving time</td>
</tr><tr>
<td>storagelo cation</td>
<td>VARC<br>HAR(5 0)</td>
<td>NOT NULL</td>
<td>-</td>
<td>Storage location, e.g., "Raw<br>Material Warehouse Area A,<br>Shelf 3, Layer 2"</td>
</tr><tr>
<td>usedreco rds</td>
<td>JSONB</td>
<td>NOT NULL</td>
<td>0</td>
<td>Usage records,e.g.,<br>[{"workorderid":"WO2025001","usedqty":10,"usetime":"2025-11-20 08:30:00"}]</td>
</tr><tr>
<td>remaining qty</td>
<td>DECIM AL(10, 2)</td>
<td>NOT NULL</td>
<td>0.00</td>
<td>Remaining quantity, unit<br>matches raw material type</td>
</tr><tr>
<td>tracestatu S</td>
<td>VARC<br>HAR(1 5)</td>
<td>NOT NULL,<br>CHECK IN ('In<br>Stock','In<br>Use','Consumed', 'Scrapped')</td>
<td>'In Stock'</td>
<td>Traceability status</td>
</tr></table>

# 5.2.2 Batch Trace Relation Table (batchtracerelation)

<table border="1" ><tr>
<td>Field Name</td>
<td>Data<br>Type</td>
<td>Constraint Conditions</td>
<td>Default Value</td>
<td>Remark<br>Description</td>
</tr><tr>
<td>relationid</td>
<td>VARCH AR(32)</td>
<td>PK, NOT NULL, UNIQUE</td>
<td>-</td>
<td>Relation ID,<br>format "BTR-<br>YYYYMMDD-<br>XXXXXX"</td>
</tr><tr>
<td>productbat chno</td>
<td>VARCH<br>AR(20)</td>
<td>NOT NULL</td>
<td>-</td>
<td>Finished<br>product batch<br>number</td>
</tr><tr>
<td>producttrac ecode</td>
<td>VARCH<br>AR(36)</td>
<td>NOT NULL, UNIQUE</td>
<td>-</td>
<td>Unique<br>traceability<br>code of finished product</td>
</tr><tr>
<td>materialtra cecode</td>
<td>VARCH AR(36)</td>
<td>FK(rawmaterialtracere cord.tracecode), NOT<br>NULL</td>
<td>-</td>
<td>Associated raw material<br>traceability<br>code</td>
</tr><tr>
<td>equipmenti d</td>
<td>VARCH<br>AR(20)</td>
<td>FK(equipment.equipment id), NOT NULL</td>
<td>-</td>
<td>Associated<br>processing<br>equipment ID</td>
</tr><tr>
<td>processsch emeid</td>
<td>VARCH<br>AR(32)</td>
<td>FK(processparamsche me.schemeid), NOT<br>NULL</td>
<td>-</td>
<td>Associated<br>process</td>
</tr><tr>
<td></td>
<td></td>
<td></td>
<td></td>
<td>parameter<br>scheme ID</td>
</tr><tr>
<td>inspectionp ersonid</td>
<td>VARCH<br>AR(20)</td>
<td>FK(employee.empid),<br>NOT NULL</td>
<td>-</td>
<td>Associated<br>inspector ID</td>
</tr><tr>
<td>inspectionti me</td>
<td>TIMEST AMP</td>
<td>NOT NULL</td>
<td>CURRENTTI MESTAMP</td>
<td>Inspection time</td>
</tr><tr>
<td>relationstag e</td>
<td>VARCH<br>AR(30)</td>
<td>NOT NULL</td>
<td>-</td>
<td>Associated<br>stage, e.g., "5-<br>axis<br>milling""drilling" "assembly"</td>
</tr><tr>
<td>relationstat us</td>
<td>VARCH<br>AR(15)</td>
<td>NOT NULL, CHECK IN<br>('Valid','Invalid','Pending<br>Confirmation')</td>
<td>'Valid'</td>
<td>Relation status</td>
</tr></table>

**5.2.3 Quality Risk Warning Table (qualityriskwarning)**

<table border="1" ><tr>
<td>Field Name</td>
<td>Data Type</td>
<td>Constraint<br>Conditions</td>
<td>Default Value</td>
<td>Remark<br>Description</td>
</tr><tr>
<td>warningid</td>
<td>VARCHAR( 32)</td>
<td>PK, NOT NULL,<br>UNIQUE</td>
<td>-</td>
<td>Warning ID,<br>format "QRW-<br>YYYYMMDD-<br>XXXXXX"</td>
</tr><tr>
<td>warningobj ect</td>
<td>VARCHAR( 15)</td>
<td>NOT NULL,<br>CHECK IN ('Raw Material','Semi-<br>Finished<br>Product','Finished Product')</td>
<td>-</td>
<td>Warning object<br>type</td>
</tr><tr>
<td>objectid</td>
<td>VARCHAR( 32)</td>
<td>NOT NULL</td>
<td>-</td>
<td>Warning object ID, associated<br>with the primary key of the<br>corresponding<br>table</td>
</tr><tr>
<td>risktype</td>
<td>VARCHAR( 50)</td>
<td>NOT NULL</td>
<td>-</td>
<td>Risk type,e.g.,<br>"Aluminum alloy silicon content<br>deviation""dime nsion out-of-<br>tolerance"</td>
</tr><tr>
<td>risklevel</td>
<td>INT</td>
<td>NOT NULL,<br>CHECK(risklevel BETWEEN 1<br>AND 5)</td>
<td>3</td>
<td>Risk level, Level<br>5 is the highest</td>
</tr><tr>
<td>triggercondi tion</td>
<td>TEXT</td>
<td>NOT NULL</td>
<td>-</td>
<td>Warning trigger condition,e.g.,<br>"Silicon content standard value<br>0.5%-0.8%,<br>actual value<br>0.82%"</td>
</tr><tr>
<td>triggertime</td>
<td>TIMESTAM P</td>
<td>NOT NULL</td>
<td>CURRENTTIMES TAMP</td>
<td>Warning trigger time</td>
</tr><tr>
<td>handlerid</td>
<td>VARCHAR( 20)</td>
<td>FK(employee.em<br>pid), NOT NULL</td>
<td>-</td>
<td>Handler ID</td>
</tr><tr>
<td>handlestatu S</td>
<td>VARCHAR( 15)</td>
<td>NOT NULL,<br>CHECK IN<br>('Pending<br>Handling','In<br>Handling','Closed' )</td>
<td>'Pending Handling'</td>
<td>Handling status</td>
</tr><tr>
<td>handleresul t</td>
<td>TEXT</td>
<td>NULL</td>
<td>-</td>
<td>Handling result, only has value<br>for closed status</td>
</tr></table>

# 5.3 Graph Database Traceability Relation Design (Neo4j)

The graph structure is used to store full-link traceability relationships, and fast traceability queries are realized through the association between nodes and edges. The specific design is as follows:

<table border="1" ><tr>
<td>Node Type</td>
<td>Core Attributes</td>
<td>Associated<br>Node Types</td>
<td>Edge Type</td>
<td>Edge Attributes</td>
</tr><tr>
<td>Supplier</td>
<td>supplierid,<br>name,<br>qualificationstatu S</td>
<td>RawMaterial</td>
<td>Provide</td>
<td>providetime,<br>batchno</td>
</tr><tr>
<td>RawMaterial</td>
<td>tracecode,<br>materialtype,<br>batchno</td>
<td>SemiProduct</td>
<td>ProcessTo</td>
<td>processtime,<br>equipmentid,<br>processschemei d</td>
</tr><tr>
<td>SemiProduct</td>
<td>tracecode,<br>producttype,<br>batchno</td>
<td>FinishedProdu ct</td>
<td>AssembleT O</td>
<td>assembletime,<br>inspectionid,<br>inspectorid</td>
</tr><tr>
<td>FinishedProdu<br>ct</td>
<td>tracecode,<br>productmodel,<br>batchno</td>
<td>Customer</td>
<td>DeliverTo</td>
<td>delivertime,<br>orderid,<br>deliveryno</td>
</tr><tr>
<td>Customer</td>
<td>customerid,<br>name,<br>industrytype</td>
<td>-</td>
<td>-</td>
<td>-</td>
</tr></table>

Query Example: When querying the full link through the finished product traceability code, you can directly traverse the associated edges of "FinishedProduct → SemiProduct→RawMaterial → Supplier" and return the complete traceability chain and the attribute information of each link in milliseconds.

# VI. Data Integration and Circulation Design

## 6.1 Data Integration Architecture

A full-link data integration architecture of "external collaboration - internal integration-intelligent analysis - business application" is constructed. The core components include:

1. External Collaboration Layer: Deploy a supplier portal system, which connects with core supplier systems through an API gateway; adopt the EDIFACT standard protocol to interact with aviation customer systems to realize the synchronization of order and delivery data.

2. Internal Integration Layer: Use Apache Kafka as a message queue to realize high-reliability transmission of data from systems such as ERP, MES, WMS, and QMS; process real-time data streams through Apache Flink to complete data cleaning and associated calculation.

3. Intelligent Analysis Layer: Build a quality risk prediction model based on Python Scikit-learn, input raw material attributes and inspection data, and output risk levels; realize optimized query of traceability links through Neo4j graph algorithms.

4. Business Application Layer: Provide standardized RESTful APIs for procurement management systems, quality traceability systems, and supply chain collaboration platforms to support data query and business triggering.

## 6.2 Core Data Circulation Processes

### 6.2.1 Full-Link Traceability Data Circulation Process

1. When raw materials enter the factory, the procurement system generates a unique traceability code, associates the supplier batch number and purchase order information, and synchronizes them to the Raw Material Trace Record Table.

2. After the completion of incoming inspection, the QMS system binds the inspection data with the traceability code, synchronizes it to the Quality Inspection Data Table; if the inspection is abnormal, a quality risk warninggis triggered.

3. When raw materials are collected to the production workshop, the MES system records the collection information, updates the usedrecords field of the Raw Material Trace Record Table, and generates a semi-finished product traceability code.

4. During the production process, the system automatically associates the raw material traceability code, processing equipment, and process parameters, establishes an association relationship through the Batch Trace Relation Table, and synchronizes it to the Neo4j graph database.

5. After the finished product is completed, a unique traceability code for the finished product is generated, which is bound to the semi-finished product traceability code through the Batch Trace Relation Table to form a complete traceability chain of "supplier - raw material - semi-finished product - finished product".

6. When the finished product is delivered, the delivery information is associated with the finished product traceability code and synchronized to the customer system to support traceability query on the customer side.

### 6.2.2 Quality Risk Warning Process

1. After the completion of incoming raw material inspection or in-process inspection, the inspection data is transmitted to the Flink processing node through Kafka.

2. Flink performs real-time comparison on the inspection data according to the preset quality standard thresholds (such as material composition range, dimensional tolerance).

3. When the inspection data exceeds the threshold, the system automatically calculates the risk level, generates a quality risk warning record, and synchronizes it to the Quality Risk Warning Table.

4. The system pushes the warning information to the handler via SMS, email, and system messages, and highlights it in the quality traceability system.

5. After the handler completes the processing, he uipdates the handling status and handling result of the warning record, and the system automatically records the handling log.

6. Conduct statistical analysis on the quality risk warning data every month, and output a supplier quality performance report for supplier optimization management.

# VII. Data Security and Permission Management

## 7.1 Permission Management System

Based on the RBAC model, supply chain and quality-specific permissions are expanded to realize three-dimensional permission control of "data type + operation scope + business scenario":

<table border="1" ><tr>
<td>Role Type</td>
<td>Data Access Scope</td>
<td>Core Operation<br>Permissions</td>
<td>Typical Positions</td>
</tr><tr>
<td>Procurement<br>Specialist</td>
<td>Supplier archives,<br>purchase orders,<br>raw material<br>traceability data</td>
<td>Supplier information entry,purchase<br>order creation, raw<br>material receiving<br>confirmation</td>
<td>Procurement<br>Engineer</td>
</tr><tr>
<td>Quality Specialist</td>
<td>Quality inspection<br>data,risk warnings, traceability records</td>
<td>Inspection data<br>entry,warning<br>handling, traceability query, quality report generation</td>
<td>Quality Engineer</td>
</tr><tr>
<td>Supply Chain<br>Manager</td>
<td>Collaboration plans, delivery data,<br>inventory<br>information</td>
<td>Collaboration plan<br>formulation, delivery progress tracking,<br>inventory query</td>
<td>Supply Chain<br>Manager</td>
</tr><tr>
<td>Production Operator</td>
<td>Usage records,<br>production link<br>traceability data</td>
<td>Raw material<br>collection<br>confirmation,<br>production data<br>entry</td>
<td>Workshop Operator</td>
</tr><tr>
<td>Audit Specialist</td>
<td>Full traceability data, operation logs</td>
<td>Traceability query,<br>log audit,<br>compliance report<br>generation</td>
<td>Internal Auditor</td>
</tr></table>

## 7.2 Data Security Assurance Measures

1. Data Transmission Security: Supplier data is transmitted through VPN encrypted tunnels, and API calls adopt the OAuth 2.0 authentication + JWT token mechanism to prevent illegal data theft.

2. Data Storage Security: Core supplier data and quality data adopt Transparent Data Encryption (TDE) technology, sensitive fields arestored separately with encryption, and keys are rotated quarterly.

3. Operation Security Control: Sensitive operations (such as modification of traceability data, adjustment of quality standards) require dual-person authorization; operation logs record IP addresses, operation times, and operation contents to support audit and traceability.

4. Permission Security Protection: Permissions are assigned based on the principle of least privilege, and regular permission audits are conducted; temporary permission elevation applications are supported, and temporary permissions can be obtained only after approval.

5. External Data Security: The supplier portal system adopts two-factor authentication; customer traceability queries adopt limited permission control, and only traceability data of associated orders can be queried.

