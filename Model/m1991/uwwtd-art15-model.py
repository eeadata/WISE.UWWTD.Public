"""
SQLModel definitions for the UWWTD Article 15 dataset.
Source: https://dd.eionet.europa.eu/datasets/latest/UWWTDArt15
Dataset: Urban Waste Water Treatment Directive reporting under Article 15 (October 2025)

Table hierarchy / FK relationships:
  Reporter          <-- ReportPeriod (rptMStateKey)
  ReportPeriod      <-- Contacts, ReceivingAreasSAMain, ReceivingAreasSAParameter,
                        ReceivingAreasSA54, ReceivingAreasLSA, ReceivingAreasSASA,
                        ReceivingAreasSALSAPredecessor, Agglomerations, UWWTPs,
                        UwwtpAgglos, DischargePoints, MSLevel, Industries (repCode)
  ReceivingAreasSAMain  <-- ReceivingAreasSAParameter, ReceivingAreasSA54,
                            ReceivingAreasSASA, DischargePoints (rcaCode)
  ReceivingAreasLSA     <-- ReceivingAreasSASA, ReceivingAreasSALSAPredecessor (rcaCode)
  Agglomerations    <-- UWWTPs, UwwtpAgglos (aggCode)
  UWWTPs            <-- UwwtpAgglos, DischargePoints (uwwCode)
"""

from datetime import date
from decimal import Decimal
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


# ---------------------------------------------------------------------------
# Reporter
# ---------------------------------------------------------------------------


class Reporter(SQLModel, table=True):
    """Information on reporting state and language of the report."""

    __tablename__ = "Reporter"

    rptMStateKey: str = Field(
        primary_key=True,
        description="Abbreviation of EEA Member State or Collaborating Country.",
    )
    rptMStateValue: Optional[str] = Field(
        default=None,
        description="Member State or Collaborating Country name.",
    )
    rptCulture: Optional[str] = Field(
        default=None,
        description="Culture code and language of the report.",
    )

    # Relationships
    report_periods: List["ReportPeriod"] = Relationship(back_populates="reporter")


# ---------------------------------------------------------------------------
# ReportPeriod
# ---------------------------------------------------------------------------


class ReportPeriod(SQLModel, table=True):
    """Specifies country, report ID, version, and reference year."""

    __tablename__ = "ReportPeriod"

    repCode: str = Field(
        primary_key=True,
        description="Report ID as specified by country.",
    )
    rptMStateKey: str = Field(
        foreign_key="Reporter.rptMStateKey",
        description="FK → Reporter.rptMStateKey",
    )
    repVersion: date = Field(
        description="Version of reported data (date of reporting)."
    )
    repSituationAt: date = Field(
        description="End date of the period for which data was reported."
    )
    repReportedPeriod: int = Field(description="Reported year.")
    repReferenceSystem: str = Field(
        description="Reference system used for reporting spatial data."
    )

    # Relationships
    reporter: Optional[Reporter] = Relationship(back_populates="report_periods")
    contacts: List["Contacts"] = Relationship(back_populates="report_period")
    receiving_areas_sa_main: List["ReceivingAreasSAMain"] = Relationship(
        back_populates="report_period"
    )
    receiving_areas_sa_parameter: List["ReceivingAreasSAParameter"] = Relationship(
        back_populates="report_period"
    )
    receiving_areas_sa54: List["ReceivingAreasSA54"] = Relationship(
        back_populates="report_period"
    )
    receiving_areas_lsa: List["ReceivingAreasLSA"] = Relationship(
        back_populates="report_period"
    )
    receiving_areas_sasa: List["ReceivingAreasSASA"] = Relationship(
        back_populates="report_period"
    )
    receiving_areas_salsa_predecessor: List["ReceivingAreasSALSAPredecessor"] = (
        Relationship(back_populates="report_period")
    )
    agglomerations: List["Agglomerations"] = Relationship(
        back_populates="report_period"
    )
    uwwtps: List["UWWTPs"] = Relationship(back_populates="report_period")
    uwwtp_agglos: List["UwwtpAgglos"] = Relationship(back_populates="report_period")
    discharge_points: List["DischargePoints"] = Relationship(
        back_populates="report_period"
    )
    ms_level: Optional["MSLevel"] = Relationship(back_populates="report_period")
    industries: List["Industries"] = Relationship(back_populates="report_period")


# ---------------------------------------------------------------------------
# Contacts
# ---------------------------------------------------------------------------


class Contacts(SQLModel, table=True):
    """Contact person responsible for data provision."""

    __tablename__ = "Contacts"

    # Surrogate PK — the source schema has no explicit PK on this table;
    # repCode + conEmail is a natural candidate key.
    id: Optional[int] = Field(default=None, primary_key=True)

    repCode: str = Field(
        foreign_key="ReportPeriod.repCode",
        description="FK → ReportPeriod.repCode",
    )
    conName: str = Field(description="Reporting contact name.")
    conInstitution: str = Field(
        description="Name of institution to which the data provider is affiliated."
    )
    conStreet: Optional[str] = Field(default=None, description="Street address.")
    conZIP: Optional[str] = Field(default=None, description="Post code.")
    conCity: Optional[str] = Field(default=None, description="City.")
    conPhone: str = Field(description="Phone number.")
    conEmail: str = Field(description="Contact person e-mail address.")
    conRemarks: Optional[str] = Field(default=None, description="Remarks.")

    # Relationships
    report_period: Optional[ReportPeriod] = Relationship(back_populates="contacts")


# ---------------------------------------------------------------------------
# ReceivingAreasSAMain
# ---------------------------------------------------------------------------


class ReceivingAreasSAMain(SQLModel, table=True):
    """Basic attributes of sensitive areas and catchments."""

    __tablename__ = "ReceivingAreasSAMain"

    rcaCode: str = Field(
        primary_key=True,
        description="ID of the sensitive area.",
    )
    repCode: str = Field(
        foreign_key="ReportPeriod.repCode",
        description="FK → ReportPeriod.repCode",
    )
    rcaName: str = Field(description="Name of the sensitive area.")
    rcaZtype: str = Field(description="Type of receiving area.")
    rcaSpZTyp: str = Field(description="Sub-type of receiving area.")
    rcaParameterN: bool = Field(
        description="Parameters subject to More Stringent Treatment: N."
    )
    rcaParameterP: bool = Field(
        description="Parameters subject to More Stringent Treatment: P."
    )
    rcaParameterM: bool = Field(
        description="Parameters subject to More Stringent Treatment: M."
    )
    rcaParameterOther: bool = Field(
        description="Parameters subject to More Stringent Treatment: Other."
    )
    rcaArt58DateDesign: Optional[date] = Field(
        default=None,
        description="Date of designation of Art. 5(8) of the UWWTD.",
    )
    rcaDateArt58: Optional[date] = Field(
        default=None,
        description="Starting date of application of Art. 5(8) of the UWWTD.",
    )
    rcaDateArt54: Optional[date] = Field(
        default=None,
        description="Starting date of application of Art. 5(4) of the UWWTD.",
    )
    rcaHyperlink: Optional[str] = Field(
        default=None, description="Hyperlink to a national webpage."
    )
    rcaBeginLife: Optional[date] = Field(
        default=None, description="Begin lifespan version."
    )
    rcaEndLife: Optional[date] = Field(
        default=None, description="End lifespan version."
    )
    rcaRemarks: Optional[str] = Field(default=None, description="Remarks.")

    # Relationships
    report_period: Optional[ReportPeriod] = Relationship(
        back_populates="receiving_areas_sa_main"
    )
    parameters: List["ReceivingAreasSAParameter"] = Relationship(
        back_populates="receiving_area_main"
    )
    sa54_data: Optional["ReceivingAreasSA54"] = Relationship(
        back_populates="receiving_area_main"
    )
    sa_sa_links: List["ReceivingAreasSASA"] = Relationship(
        back_populates="receiving_area_main"
    )
    discharge_points: List["DischargePoints"] = Relationship(
        back_populates="receiving_area_main"
    )


# ---------------------------------------------------------------------------
# ReceivingAreasSAParameter
# ---------------------------------------------------------------------------


class ReceivingAreasSAParameter(SQLModel, table=True):
    """Designation criteria, dates and deadlines for sensitive areas."""

    __tablename__ = "ReceivingAreasSAParameter"

    # Composite PK: rcaCode + rcaParameter
    rcaCode: str = Field(
        primary_key=True,
        foreign_key="ReceivingAreasSAMain.rcaCode",
        description="FK (PK) → ReceivingAreasSAMain.rcaCode",
    )
    rcaParameter: str = Field(
        primary_key=True,
        description="Name of the receiving area parameter (PK).",
    )
    repCode: str = Field(
        foreign_key="ReportPeriod.repCode",
        description="FK → ReportPeriod.repCode",
    )
    rcaDateDesignation: date = Field(description="Date of designation.")
    rcaStartDate: Optional[date] = Field(
        default=None, description="Starting date of application."
    )
    rcaCRelevantDirective: Optional[str] = Field(
        default=None,
        description="Designation criteria c – relevant EU Directives and related parameters.",
    )
    rcaCIDOtherDirective: Optional[str] = Field(
        default=None,
        description="Designation criteria c – ID applied to the area under this Directive.",
    )
    rcaCDateOtherDirective: Optional[date] = Field(
        default=None,
        description="Designation criteria c – reference date of the area under this Directive.",
    )

    # Relationships
    report_period: Optional[ReportPeriod] = Relationship(
        back_populates="receiving_areas_sa_parameter"
    )
    receiving_area_main: Optional[ReceivingAreasSAMain] = Relationship(
        back_populates="parameters"
    )


# ---------------------------------------------------------------------------
# ReceivingAreasSA54
# ---------------------------------------------------------------------------


class ReceivingAreasSA54(SQLModel, table=True):
    """Article 5.4 specific attributes — load and plant counts per sensitive area."""

    __tablename__ = "ReceivingAreasSA54"

    rcaCode: str = Field(
        primary_key=True,
        foreign_key="ReceivingAreasSAMain.rcaCode",
        description="FK (PK) → ReceivingAreasSAMain.rcaCode",
    )
    repCode: str = Field(
        foreign_key="ReportPeriod.repCode",
        description="FK → ReportPeriod.repCode",
    )
    rcaMethod54: str = Field(
        description="Methodology of the load calculation for Art. 5.4."
    )
    rcaPlants54: int = Field(
        description="Number of UWWTPs located and discharging within the Art. 5.4 area."
    )
    rcaPlantsCapacity54: int = Field(
        description="Total organic design capacity (p.e.) of UWWTPs in the Art. 5.4 area."
    )
    rcaNIncoming54: Decimal = Field(
        description="Aggregated incoming N-tot loads (tons/year) within the Art. 5.4 area."
    )
    rcaNDischarged54: Decimal = Field(
        description="Aggregated discharged N-tot loads (tons/year) within the Art. 5.4 area."
    )
    rcaPIncoming54: Decimal = Field(
        description="Aggregated incoming P-tot loads (tons/year) within the Art. 5.4 area."
    )
    rcaPDischarged54: Decimal = Field(
        description="Aggregated discharged P-tot loads (tons/year) within the Art. 5.4 area."
    )

    # Relationships
    report_period: Optional[ReportPeriod] = Relationship(
        back_populates="receiving_areas_sa54"
    )
    receiving_area_main: Optional[ReceivingAreasSAMain] = Relationship(
        back_populates="sa54_data"
    )


# ---------------------------------------------------------------------------
# ReceivingAreasLSA
# ---------------------------------------------------------------------------


class ReceivingAreasLSA(SQLModel, table=True):
    """Attributes and designation criteria of Less Sensitive Areas."""

    __tablename__ = "ReceivingAreasLSA"

    rcaCode: str = Field(
        primary_key=True,
        description="ID of the less sensitive area.",
    )
    repCode: str = Field(
        foreign_key="ReportPeriod.repCode",
        description="FK → ReportPeriod.repCode",
    )
    rcaName: str = Field(description="Name of the less sensitive area.")
    rcaZtype: str = Field(description="Zone type code.")
    rca61DateDesignation: date = Field(
        description="Date of designation under Art. 6(1)."
    )
    rcaMorphology: Optional[bool] = Field(
        default=None,
        description="Designation criteria – Morphology (Annex II B).",
    )
    rcaHydrology: Optional[bool] = Field(
        default=None,
        description="Designation criteria – Hydrology (Annex II B).",
    )
    rcaHydraulic: Optional[bool] = Field(
        default=None,
        description="Designation criteria – Specific hydraulic conditions (Annex II B).",
    )
    rcaAbsenceRisk: Optional[bool] = Field(
        default=None,
        description="Designation criteria – Absence of risk of load transfer to adjacent areas.",
    )
    rcaHyperlink: Optional[str] = Field(
        default=None, description="Hyperlink to a national webpage."
    )
    rcaBeginLife: Optional[date] = Field(
        default=None, description="Begin lifespan version."
    )
    rcaEndLife: Optional[date] = Field(
        default=None, description="End lifespan version."
    )
    rcalsaRemarks: Optional[str] = Field(default=None, description="Remarks.")

    # Relationships
    report_period: Optional[ReportPeriod] = Relationship(
        back_populates="receiving_areas_lsa"
    )
    sa_sa_links: List["ReceivingAreasSASA"] = Relationship(
        back_populates="receiving_area_lsa"
    )
    predecessors: List["ReceivingAreasSALSAPredecessor"] = Relationship(
        back_populates="receiving_area"
    )


# ---------------------------------------------------------------------------
# ReceivingAreasSASA
# ---------------------------------------------------------------------------


class ReceivingAreasSASA(SQLModel, table=True):
    """Link between a sensitive area catchment and its corresponding sensitive area."""

    __tablename__ = "ReceivingAreasSASA"

    # Surrogate PK — the source schema has no explicit PK on this table.
    id: Optional[int] = Field(default=None, primary_key=True)

    repCode: str = Field(
        foreign_key="ReportPeriod.repCode",
        description="FK → ReportPeriod.repCode",
    )
    rcaCode: str = Field(
        foreign_key="ReceivingAreasSAMain.rcaCode",
        description="ID of the sensitive area catchment (FK → ReceivingAreasSAMain).",
    )
    rcaRelatedSA: str = Field(
        foreign_key="ReceivingAreasLSA.rcaCode",
        description="ID of the related sensitive area (FK → ReceivingAreasLSA).",
    )
    rcaRelatedSARemark: Optional[str] = Field(default=None, description="Remark.")

    # Relationships
    report_period: Optional[ReportPeriod] = Relationship(
        back_populates="receiving_areas_sasa"
    )
    receiving_area_main: Optional[ReceivingAreasSAMain] = Relationship(
        back_populates="sa_sa_links"
    )
    receiving_area_lsa: Optional[ReceivingAreasLSA] = Relationship(
        back_populates="sa_sa_links"
    )


# ---------------------------------------------------------------------------
# ReceivingAreasSALSAPredecessor
# ---------------------------------------------------------------------------


class ReceivingAreasSALSAPredecessor(SQLModel, table=True):
    """Predecessors of deactivated sensitive or less-sensitive receiving areas."""

    __tablename__ = "ReceivingAreasSALSAPredecessor"

    # Surrogate PK — the source schema has no explicit PK on this table.
    id: Optional[int] = Field(default=None, primary_key=True)

    repCode: str = Field(
        foreign_key="ReportPeriod.repCode",
        description="FK → ReportPeriod.repCode",
    )
    rcaCode: str = Field(
        foreign_key="ReceivingAreasLSA.rcaCode",
        description="ID code of the existing sensitive or less-sensitive area.",
    )
    rcaCodePredecessor: str = Field(
        description="ID code of the area that is no longer operational."
    )
    rcaEvolutionType: str = Field(
        description="Reason for the link between existing ID and the deactivated ID."
    )
    rcasalsaRemark: Optional[str] = Field(default=None, description="Remark.")

    # Relationships
    report_period: Optional[ReportPeriod] = Relationship(
        back_populates="receiving_areas_salsa_predecessor"
    )
    receiving_area: Optional[ReceivingAreasLSA] = Relationship(
        back_populates="predecessors"
    )


# ---------------------------------------------------------------------------
# Agglomerations
# ---------------------------------------------------------------------------


class Agglomerations(SQLModel, table=True):
    """Agglomerations ≥ 2 000 p.e.: load, collection rates, and compliance dates."""

    __tablename__ = "Agglomerations"

    aggCode: str = Field(
        primary_key=True,
        description="ID of the agglomeration as specified by country.",
    )
    aggState: int = Field(description="Status of the agglomeration.")
    repCode: str = Field(
        foreign_key="ReportPeriod.repCode",
        description="FK → ReportPeriod.repCode",
    )
    aggName: str = Field(description="Name of the agglomeration.")
    aggNUTS: Optional[str] = Field(
        default=None, description="NUTS territorial unit code."
    )
    aggLatitude: Optional[Decimal] = Field(
        default=None, description="Latitude (ETRS89 or WGS-84, decimal degrees)."
    )
    aggLongitude: Optional[Decimal] = Field(
        default=None, description="Longitude (ETRS89 or WGS-84, decimal degrees)."
    )
    aggGenerated: int = Field(
        description="Generated load (p.e.) – size of the agglomeration."
    )
    bigCityID: Optional[str] = Field(
        default=None, description="ID of the big city / big discharger."
    )
    aggCalculation: Optional[str] = Field(
        default=None,
        description="Methods used for calculation of the generated load.",
    )
    aggChanges: Optional[bool] = Field(
        default=None,
        description="Significant changes of the generated load since the previous report.",
    )
    aggChangesComment: Optional[str] = Field(
        default=None,
        description="Explanation of significant changes compared to the previous reported load.",
    )
    aggPeriodOver: date = Field(
        description="Overall deadline for implementation of the UWWTD in this agglomeration."
    )
    aggDateArt3: date = Field(
        description="Deadline for implementation of Art. 3 requirements."
    )
    aggDateArt4: Optional[date] = Field(
        default=None,
        description="Deadline for implementation of Art. 4 requirements.",
    )
    aggDateArt5: Optional[date] = Field(
        default=None,
        description="Deadline for implementation of Art. 5 requirements.",
    )
    aggC1: Optional[Decimal] = Field(
        default=None,
        description="Rate of generated load collected through collecting system (%).",
    )
    aggMethodC1: Optional[str] = Field(
        default=None, description="Method of determination for aggC1."
    )
    aggC2: Optional[Decimal] = Field(
        default=None,
        description="Rate of generated load addressed via IAS (%).",
    )
    aggMethodC2: Optional[str] = Field(
        default=None, description="Method of determination for aggC2."
    )
    aggPercWithoutTreatment: Optional[Decimal] = Field(
        default=None,
        description="Rate of generated load not collected and not addressed via IAS (%).",
    )
    aggMethodWithoutTreatment: Optional[str] = Field(
        default=None,
        description="Method of determination for aggPercWithoutTreatment.",
    )
    aggPercPrimTreatment: Optional[Decimal] = Field(
        default=None,
        description="Share (%) of load addressed via IAS receiving primary treatment.",
    )
    aggPercSecTreatment: Optional[Decimal] = Field(
        default=None,
        description="Share (%) of load addressed via IAS receiving secondary treatment.",
    )
    aggPercStringentTreatment: Optional[Decimal] = Field(
        default=None,
        description="Share (%) of load addressed via IAS receiving more stringent treatment.",
    )
    aggHaveRegistrationSystem: Optional[bool] = Field(
        default=None,
        description="Is a registration system for leaks in collecting system in place?",
    )
    aggExistMaintenancePlan: Optional[bool] = Field(
        default=None,
        description="Is a maintenance plan for collecting system in place?",
    )
    aggPressureTest: Optional[bool] = Field(
        default=None,
        description="Have pressure tests been used to maintain collecting systems?",
    )
    aggVideoInspections: Optional[bool] = Field(
        default=None,
        description="Have regular video inspections been used to maintain collecting systems?",
    )
    aggOtherMeasures: Optional[bool] = Field(
        default=None,
        description="Have other measures been used to maintain collecting systems?",
    )
    aggExplanationOther: Optional[str] = Field(
        default=None, description="Short explanation of other measures."
    )
    aggSewageNetwork: Optional[str] = Field(
        default=None, description="Type of collecting system."
    )
    aggBestTechnicalKnowledge: Optional[bool] = Field(
        default=None,
        description="Is best technical knowledge to limit pollution applied?",
    )
    aggDilutionRates: Optional[bool] = Field(
        default=None,
        description="Have dilution rate measures been used to limit pollution?",
    )
    aggCapacity: Optional[bool] = Field(
        default=None,
        description="Have capacity in relation to dry weather flow measures been used?",
    )
    aggAccOverflows: Optional[bool] = Field(
        default=None,
        description="Have acceptable number of overflows per year measures been used?",
    )
    aggAccOverflowNumber: Optional[int] = Field(
        default=None, description="Number of overflows per year."
    )
    aggSewerOverflows_m3: Optional[int] = Field(
        default=None,
        description="Annual volume of raw sewage via CSOs (m³/year).",
    )
    aggSewerOverflows_pe: Optional[int] = Field(
        default=None,
        description="Annual load of raw sewage via CSOs (p.e.).",
    )
    aggForecast: Optional[date] = Field(
        default=None,
        description="Date by when total generated load will be fully collected or addressed via IAS.",
    )
    aggBeginLife: Optional[date] = Field(
        default=None, description="Begin lifespan version."
    )
    aggEndLife: Optional[date] = Field(
        default=None, description="End lifespan version."
    )
    aggHyperlink: Optional[str] = Field(
        default=None,
        description="Hyperlink to national website where agglomeration can be found.",
    )
    aggRemarks: Optional[str] = Field(default=None, description="Remarks.")

    # Relationships
    report_period: Optional[ReportPeriod] = Relationship(
        back_populates="agglomerations"
    )
    uwwtps: List["UWWTPs"] = Relationship(back_populates="agglomeration")
    uwwtp_agglos: List["UwwtpAgglos"] = Relationship(back_populates="agglomeration")


# ---------------------------------------------------------------------------
# UWWTPs
# ---------------------------------------------------------------------------


class UWWTPs(SQLModel, table=True):
    """Individual waste water treatment plants and collecting systems without UWWTP."""

    __tablename__ = "UWWTPs"

    uwwCode: str = Field(
        primary_key=True,
        description="ID of wastewater treatment plant / collecting system without treatment.",
    )
    uwwState: int = Field(description="Status of the UWWTP.")
    repCode: str = Field(
        foreign_key="ReportPeriod.repCode",
        description="FK → ReportPeriod.repCode",
    )
    aggCode: Optional[str] = Field(
        default=None,
        foreign_key="Agglomerations.aggCode",
        description="FK → Agglomerations.aggCode",
    )
    uwwName: str = Field(
        description="Name of wastewater treatment plant / collecting system without treatment."
    )
    uwwCollectingSystem: str = Field(
        description="Specification of existing UWWTP (in operation) or collecting system without UWWTP."
    )
    uwwDateClosing: Optional[date] = Field(
        default=None, description="Date of closing of the UWWTP."
    )
    uwwHistorie: Optional[str] = Field(
        default=None,
        description="Reasons for closing and successor of the closed UWWTP.",
    )
    uwwLatitude: Optional[Decimal] = Field(
        default=None, description="Latitude (ETRS89 or WGS-84, decimal degrees)."
    )
    uwwLongitude: Optional[Decimal] = Field(
        default=None, description="Longitude (ETRS89 or WGS-84, decimal degrees)."
    )
    uwwNUTS: Optional[str] = Field(
        default=None, description="NUTS territorial unit code."
    )
    uwwLoadEnteringUWWTP: Optional[int] = Field(
        default=None, description="Load entering UWWTP (p.e.)."
    )
    uwwCapacity: Optional[int] = Field(
        default=None, description="Organic design capacity (p.e.)."
    )
    uwwPrimaryTreatment: Optional[bool] = Field(
        default=None, description="Primary treatment applied."
    )
    uwwSecondaryTreatment: Optional[bool] = Field(
        default=None, description="Secondary treatment applied."
    )
    uwwOtherTreatment: Optional[bool] = Field(
        default=None, description="More stringent treatment applied."
    )
    uwwNRemoval: Optional[bool] = Field(default=None, description="N-removal applied.")
    uwwPRemoval: Optional[bool] = Field(default=None, description="P-removal applied.")
    uwwUV: Optional[bool] = Field(default=None, description="UV disinfection applied.")
    uwwChlorination: Optional[bool] = Field(
        default=None, description="Chlorination applied."
    )
    uwwOzonation: Optional[bool] = Field(default=None, description="Ozonation applied.")
    uwwSandFiltration: Optional[bool] = Field(
        default=None, description="Sand filtration applied."
    )
    uwwMicroFiltration: Optional[bool] = Field(
        default=None, description="Micro filtration applied."
    )
    uwwOther: Optional[bool] = Field(
        default=None, description="Other more stringent treatment applied."
    )
    uwwSpecification: Optional[str] = Field(
        default=None, description="Specification of other more stringent treatment."
    )
    uwwBOD5Perf: Optional[str] = Field(
        default=None, description="Treatment performance: BOD5."
    )
    uwwCODPerf: Optional[str] = Field(
        default=None, description="Treatment performance: COD."
    )
    uwwTSSPerf: Optional[str] = Field(
        default=None, description="Treatment performance: TSS."
    )
    uwwNTotPerf: Optional[str] = Field(
        default=None, description="Treatment performance: N."
    )
    uwwPTotPerf: Optional[str] = Field(
        default=None, description="Treatment performance: P."
    )
    uwwOtherPerf: Optional[str] = Field(
        default=None, description="Treatment performance: Others."
    )
    uwwBadPerformance: Optional[bool] = Field(
        default=None, description="Cause of failure: bad performance."
    )
    uwwAccidents: Optional[bool] = Field(
        default=None, description="Cause of failure: major accidents."
    )
    uwwBadDesign: Optional[bool] = Field(
        default=None, description="Cause of failure: bad design or dimensioning."
    )
    uwwInformation: Optional[str] = Field(
        default=None,
        description="Further information on cause of failure.",
    )
    # Incoming loads (tons/year)
    uwwBODIncomingMeasured: Optional[Decimal] = Field(default=None)
    uwwBODIncomingCalculated: Optional[Decimal] = Field(default=None)
    uwwBODIncomingEstimated: Optional[Decimal] = Field(default=None)
    uwwCODIncomingMeasured: Optional[Decimal] = Field(default=None)
    uwwCODIncomingCalculated: Optional[Decimal] = Field(default=None)
    uwwCODIncomingEstimated: Optional[Decimal] = Field(default=None)
    uwwNIncomingMeasured: Optional[Decimal] = Field(default=None)
    uwwNIncomingCalculated: Optional[Decimal] = Field(default=None)
    uwwNIncomingEstimated: Optional[Decimal] = Field(default=None)
    uwwPIncomingMeasured: Optional[Decimal] = Field(default=None)
    uwwPIncomingCalculated: Optional[Decimal] = Field(default=None)
    uwwPIncomingEstimated: Optional[Decimal] = Field(default=None)
    # Discharged loads (tons/year)
    uwwBODDischargeMeasured: Optional[Decimal] = Field(default=None)
    uwwBODDischargeCalculated: Optional[Decimal] = Field(default=None)
    uwwBODDischargeEstimated: Optional[Decimal] = Field(default=None)
    uwwCODDischargeMeasured: Optional[Decimal] = Field(default=None)
    uwwCODDischargeCalculated: Optional[Decimal] = Field(default=None)
    uwwCODDischargeEstimated: Optional[Decimal] = Field(default=None)
    uwwNDischargeMeasured: Optional[Decimal] = Field(default=None)
    uwwNDischargeCalculated: Optional[Decimal] = Field(default=None)
    uwwNDischargeEstimated: Optional[Decimal] = Field(default=None)
    uwwPDischargeMeasured: Optional[Decimal] = Field(default=None)
    uwwPDischargeCalculated: Optional[Decimal] = Field(default=None)
    uwwPDischargeEstimated: Optional[Decimal] = Field(default=None)
    # Volume / reuse
    uwwWasteWaterTreated: Optional[Decimal] = Field(
        default=None,
        description="Mean annual volume of waste water treated (m³/year).",
    )
    uwwMethodWasteWaterTreated: Optional[str] = Field(
        default=None,
        description="Method used to determine the volume of waste water treated.",
    )
    uwwWasteWaterReuse: Optional[Decimal] = Field(
        default=None,
        description="Treated waste water reused as annual mean percentage.",
    )
    uwwBeginLife: Optional[date] = Field(
        default=None, description="Begin lifespan version."
    )
    uwwEndLife: Optional[date] = Field(
        default=None, description="End lifespan version."
    )
    uwwHyperlink: Optional[str] = Field(
        default=None,
        description="Hyperlink to national website for this UWWTP.",
    )
    uwwInspireIDFacility: Optional[str] = Field(
        default=None,
        description="Code of the treatment plant used in E-PRTR reporting.",
    )
    uwwRemarks: Optional[str] = Field(default=None, description="Remarks.")

    # Relationships
    report_period: Optional[ReportPeriod] = Relationship(back_populates="uwwtps")
    agglomeration: Optional[Agglomerations] = Relationship(back_populates="uwwtps")
    uwwtp_agglos: List["UwwtpAgglos"] = Relationship(back_populates="uwwtp")
    discharge_points: List["DischargePoints"] = Relationship(back_populates="uwwtp")


# ---------------------------------------------------------------------------
# UwwtpAgglos  (junction / connection table)
# ---------------------------------------------------------------------------


class UwwtpAgglos(SQLModel, table=True):
    """
    Connection table linking UWWTPs to agglomerations (supports 1:n, m:1, n:m).
    """

    __tablename__ = "UwwtpAgglos"

    # Surrogate PK — natural key is (aucUwwCode, aucAggCode).
    id: Optional[int] = Field(default=None, primary_key=True)

    repCode: str = Field(
        foreign_key="ReportPeriod.repCode",
        description="FK → ReportPeriod.repCode",
    )
    aucUwwCode: str = Field(
        foreign_key="UWWTPs.uwwCode",
        description="FK → UWWTPs.uwwCode",
    )
    aucUwwName: Optional[str] = Field(
        default=None, description="Name of the UWWTP (denormalised copy)."
    )
    aucAggCode: str = Field(
        foreign_key="Agglomerations.aggCode",
        description="FK → Agglomerations.aggCode",
    )
    aucAggName: Optional[str] = Field(
        default=None, description="Name of the agglomeration (denormalised copy)."
    )
    aucPercEnteringUWWTP: Optional[Decimal] = Field(
        default=None,
        description="Share (%) of generated load entering this particular plant.",
    )
    aucMethodPercEnteringUWWTP: Optional[str] = Field(
        default=None, description="Method used to obtain the % value."
    )
    aucPercC2T: Optional[Decimal] = Field(
        default=None,
        description="Rate of generated load transported to this UWWTP by trucks (%).",
    )

    # Relationships
    report_period: Optional[ReportPeriod] = Relationship(back_populates="uwwtp_agglos")
    uwwtp: Optional[UWWTPs] = Relationship(back_populates="uwwtp_agglos")
    agglomeration: Optional[Agglomerations] = Relationship(
        back_populates="uwwtp_agglos"
    )


# ---------------------------------------------------------------------------
# DischargePoints
# ---------------------------------------------------------------------------


class DischargePoints(SQLModel, table=True):
    """Individual discharge points from treatment plants or collecting systems."""

    __tablename__ = "DischargePoints"

    dcpCode: str = Field(
        primary_key=True,
        description="ID of the discharge point.",
    )
    dcpState: int = Field(description="Status of the discharge point.")
    repCode: str = Field(
        foreign_key="ReportPeriod.repCode",
        description="FK → ReportPeriod.repCode",
    )
    uwwCode: str = Field(
        foreign_key="UWWTPs.uwwCode",
        description="FK → UWWTPs.uwwCode",
    )
    dcpName: str = Field(description="Name of the discharge point.")
    dcpNUTS: Optional[str] = Field(
        default=None, description="NUTS territorial unit code."
    )
    dcpLatitude: Optional[Decimal] = Field(
        default=None, description="Latitude (ETRS89 or WGS-84, decimal degrees)."
    )
    dcpLongitude: Optional[Decimal] = Field(
        default=None, description="Longitude (ETRS89 or WGS-84, decimal degrees)."
    )
    dcpWaterBodyType: str = Field(
        description="Type of water body into which waste water is discharged."
    )
    dcpIrrigation: Optional[str] = Field(
        default=None, description="Purpose of discharge on land."
    )
    dcpTypeOfReceivingArea: str = Field(
        description="Type of receiving area into which treated wastewater is discharged."
    )
    rcaCode: Optional[str] = Field(
        default=None,
        foreign_key="ReceivingAreasSAMain.rcaCode",
        description="FK → ReceivingAreasSAMain.rcaCode (ID of sensitive or less-sensitive area).",
    )
    dcpSurfaceWaters: bool = Field(description="Are there surface waters available?")
    dcpWaterbodyID: Optional[str] = Field(
        default=None, description="ID of WFD waterbody."
    )
    dcpNotAffect: Optional[bool] = Field(
        default=None,
        description="Do comprehensive studies indicate the discharge does not adversely affect the environment?",
    )
    dcpMSProvide: Optional[bool] = Field(
        default=None,
        description="Has the Member State provided these studies to the Commission?",
    )
    dcpCOMAccept: Optional[bool] = Field(
        default=None,
        description="Did the Commission formally accept that Art. 6(2) conditions are met?",
    )
    dcpGroundWater: Optional[str] = Field(
        default=None, description="ID of WFD groundwater body."
    )
    dcpReceivingWater: Optional[str] = Field(
        default=None, description="ID of receiving water."
    )
    dcpWFDSubUnit: str = Field(
        description="ID of WFD sub-unit of river basin district."
    )
    dcpWFDRBD: str = Field(description="ID of WFD river basin district.")
    dcpWaterBodyReferenceDate: Optional[date] = Field(
        default=None, description="Reference date of the WFD water body."
    )
    dcpGroundWaterReferenceDate: Optional[date] = Field(
        default=None, description="Reference date of the WFD groundwater body."
    )
    dcpReceivingWaterReferenceDate: Optional[date] = Field(
        default=None, description="Reference date of the receiving water."
    )
    dcpWFDSubUnitReferenceDate: Optional[date] = Field(
        default=None,
        description="Reference date of the WFD sub-unit of river basin district.",
    )
    dcpWFDRBDReferenceDate: Optional[date] = Field(
        default=None, description="Reference date of the WFD river basin district."
    )
    dcpBeginLife: Optional[date] = Field(
        default=None, description="Begin lifespan version."
    )
    dcpEndLife: Optional[date] = Field(
        default=None, description="End lifespan version."
    )
    dcpRemarks: Optional[str] = Field(default=None, description="Remarks.")

    # Relationships
    report_period: Optional[ReportPeriod] = Relationship(
        back_populates="discharge_points"
    )
    uwwtp: Optional[UWWTPs] = Relationship(back_populates="discharge_points")
    receiving_area_main: Optional[ReceivingAreasSAMain] = Relationship(
        back_populates="discharge_points"
    )


# ---------------------------------------------------------------------------
# MSLevel
# ---------------------------------------------------------------------------


class MSLevel(SQLModel, table=True):
    """Sludge disposal and wastewater reuse aggregated at Member State level."""

    __tablename__ = "MSLevel"

    # repCode is both PK and FK here — one row per report.
    repCode: str = Field(
        primary_key=True,
        foreign_key="ReportPeriod.repCode",
        description="PK / FK → ReportPeriod.repCode",
    )
    mslSludgeProduction: Decimal = Field(
        description="Yearly production of sludge (tons of dry solids/year)."
    )
    mslDischargePipelines: Optional[Decimal] = Field(
        default=None,
        description="Sludge discharged into surface waters via pipelines (t DS/y).",
    )
    mslDischargeShips: Optional[Decimal] = Field(
        default=None,
        description="Sludge discharged into surface waters via ships (t DS/y).",
    )
    mslDischargeOthers: Optional[Decimal] = Field(
        default=None,
        description="Sludge discharged into surface waters – other methods (t DS/y).",
    )
    mslReuseSoilAgriculture: Optional[Decimal] = Field(
        default=None,
        description="Sludge re-used – soil and agriculture (t DS/y).",
    )
    mslReuseOthers: Optional[Decimal] = Field(
        default=None, description="Sludge re-used – other purposes (t DS/y)."
    )
    mslDisposalLandfill: Optional[Decimal] = Field(
        default=None, description="Sludge disposed – landfill (t DS/y)."
    )
    mslDisposalIncineration: Optional[Decimal] = Field(
        default=None, description="Sludge disposed – incineration (t DS/y)."
    )
    mslDisposalOthers: Optional[Decimal] = Field(
        default=None, description="Sludge disposed – other methods (t DS/y)."
    )
    mslWWaterTreated: Optional[Decimal] = Field(
        default=None,
        description="Total amount of treated water (millions m³/year).",
    )
    mslWWReusePerc: Optional[Decimal] = Field(
        default=None,
        description="Rate of treated waste water re-used (% of total volume treated).",
    )
    mslWWReuseAgri: Optional[Decimal] = Field(
        default=None,
        description="Percentage of treated water re-used in agriculture.",
    )
    mslWWReuseInd: Optional[Decimal] = Field(
        default=None,
        description="Percentage of treated water re-used in industry.",
    )
    mslWWReuseOther: Optional[Decimal] = Field(
        default=None,
        description="Percentage of treated water re-used for other purposes.",
    )
    mslWWReuseExplain: Optional[str] = Field(
        default=None, description="Explanation of 'other' reuse purposes."
    )
    mslRemarks: Optional[str] = Field(default=None, description="Remarks.")

    # Relationships
    report_period: Optional[ReportPeriod] = Relationship(back_populates="ms_level")


# ---------------------------------------------------------------------------
# Industries
# ---------------------------------------------------------------------------


class Industries(SQLModel, table=True):
    """Food-processing industrial plants subject to UWWTD Art. 13."""

    __tablename__ = "Industries"

    # Surrogate PK — natural key is (repCode, indCodePlant).
    id: Optional[int] = Field(default=None, primary_key=True)

    repCode: str = Field(
        foreign_key="ReportPeriod.repCode",
        description="FK → ReportPeriod.repCode",
    )
    indState: int = Field(description="Status of the plant.")
    indCodePlant: str = Field(description="ID of the food-processing industrial plant.")
    indNamePlant: Optional[str] = Field(default=None, description="Name of the plant.")
    indBranch: Optional[str] = Field(
        default=None, description="Industrial sector of food-processing."
    )
    indOrganicLoad: Optional[int] = Field(
        default=None, description="Organic load (p.e.)."
    )
    indConditions: Optional[bool] = Field(
        default=None,
        description="Do discharges from the facility respect conditions under Art. 13?",
    )
    indDateCompliance: Optional[date] = Field(
        default=None, description="Date of compliance."
    )

    # Relationships
    report_period: Optional[ReportPeriod] = Relationship(back_populates="industries")
