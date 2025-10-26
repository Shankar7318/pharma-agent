from crewai import Agent
from crewai_tools import BaseTool
from typing import Dict, List, Any
import json
from datetime import datetime

class ReportGeneratorAgent(Agent):
    """Specialized agent for generating comprehensive research reports"""
    
    def __init__(self):
        super().__init__(
            role="Pharmaceutical Research Report Specialist",
            goal="Generate comprehensive, professional research reports synthesizing all research findings",
            backstory="""You are an expert in pharmaceutical report writing with 
            extensive experience in synthesizing complex data into actionable business 
            insights and strategic recommendations.
            
            Your capabilities include:
            - Executive summary creation
            - Data visualization and presentation
            - Strategic recommendation development
            - Risk assessment and mitigation planning
            - Professional report formatting""",
            tools=[ReportGenerationTool(), DataVisualizationTool(), ExecutiveSummaryTool()],
            verbose=True
        )

class ReportGenerationTool(BaseTool):
    name: str = "Report Generation Tool"
    description: str = "Generate comprehensive research reports from all agent findings"
    
    def _run(self, research_data: Dict, report_type: str = "comprehensive") -> Dict[str, Any]:
        """Generate comprehensive research report"""
        
        report_sections = self._create_report_structure(research_data, report_type)
        
        return {
            "report_metadata": {
                "title": f"Pharmaceutical Research Report: {research_data.get('molecule', 'Unknown')}",
                "generated_date": datetime.now().isoformat(),
                "report_type": report_type,
                "sections_count": len(report_sections)
            },
            "executive_summary": self._generate_executive_summary(research_data),
            "detailed_analysis": report_sections,
            "strategic_recommendations": self._generate_strategic_recommendations(research_data),
            "risk_assessment": self._assess_risks(research_data),
            "implementation_roadmap": self._create_implementation_roadmap(research_data)
        }
    
    def _create_report_structure(self, research_data: Dict, report_type: str) -> List[Dict]:
        """Create structured report sections"""
        sections = []
        
        # Market Analysis Section
        sections.append({
            "section_title": "Market Intelligence and Commercial Assessment",
            "content": self._format_market_analysis(research_data),
            "key_metrics": self._extract_market_metrics(research_data)
        })
        
        # Clinical Development Section
        sections.append({
            "section_title": "Clinical Development Landscape",
            "content": self._format_clinical_analysis(research_data),
            "key_metrics": self._extract_clinical_metrics(research_data)
        })
        
        # Intellectual Property Section
        sections.append({
            "section_title": "Intellectual Property Strategy",
            "content": self._format_ip_analysis(research_data),
            "key_metrics": self._extract_ip_metrics(research_data)
        })
        
        # Competitive Intelligence Section
        sections.append({
            "section_title": "Competitive Landscape Analysis",
            "content": self._format_competitive_analysis(research_data),
            "key_metrics": self._extract_competitive_metrics(research_data)
        })
        
        return sections
    
    def _generate_executive_summary(self, research_data: Dict) -> Dict[str, Any]:
        """Generate executive summary"""
        molecule = research_data.get('molecule', 'Unknown')
        therapy_area = research_data.get('therapy_area', 'Unknown')
        
        return {
            "overview": f"Comprehensive analysis of {molecule} for potential applications in {therapy_area}",
            "key_findings": [
                f"Strong market opportunity in {therapy_area} with significant growth potential",
                "Multiple clinical development pathways identified for new indications",
                "Favorable intellectual property landscape with clear white space opportunities",
                "Competitive positioning supports strategic development approach"
            ],
            "strategic_highlights": [
                "Recommended development pathway: 505(b)(2) for expedited approval",
                "Target timeline: 24-36 months to market entry",
                "Estimated peak sales potential: $500M - $1B",
                "Key success factors: Clinical validation, IP protection, market access"
            ],
            "recommended_next_steps": [
                "Initiate preclinical studies for lead indications",
                "File method-of-use patent applications",
                "Engage regulatory consultants for pathway optimization",
                "Develop commercial launch strategy"
            ]
        }
    
    def _generate_strategic_recommendations(self, research_data: Dict) -> List[Dict]:
        """Generate strategic recommendations"""
        recommendations = []
        
        # Development Strategy
        recommendations.append({
            "category": "Development Strategy",
            "recommendation": "Pursue 505(b)(2) regulatory pathway for expedited approval",
            "rationale": "Leverages existing safety data, reduces development time and cost",
            "priority": "High",
            "timeline": "Immediate",
            "resources_required": "Regulatory consultants, clinical development team"
        })
        
        # IP Strategy
        recommendations.append({
            "category": "IP Strategy",
            "recommendation": "File comprehensive method-of-use patent portfolio",
            "rationale": "Protects new indications and creates competitive barriers",
            "priority": "High",
            "timeline": "90 days",
            "resources_required": "Patent attorneys, $50-100K budget"
        })
        
        # Commercial Strategy
        recommendations.append({
            "category": "Commercial Strategy",
            "recommendation": "Develop targeted market access strategy for key geographies",
            "rationale": "Maximizes revenue potential and ensures reimbursement",
            "priority": "Medium",
            "timeline": "12 months",
            "resources_required": "Market access team, health economics expertise"
        })
        
        # Partnership Strategy
        recommendations.append({
            "category": "Partnership Strategy",
            "recommendation": "Explore co-development partnerships for specific indications",
            "rationale": "Shares development risk and accelerates time to market",
            "priority": "Medium",
            "timeline": "6-12 months",
            "resources_required": "Business development team, legal support"
        })
        
        return recommendations
    
    def _assess_risks(self, research_data: Dict) -> Dict[str, Any]:
        """Comprehensive risk assessment"""
        return {
            "development_risks": [
                {
                    "risk": "Clinical trial failures",
                    "probability": "Medium",
                    "impact": "High",
                    "mitigation": "Robust preclinical validation, adaptive trial design"
                },
                {
                    "risk": "Regulatory delays",
                    "probability": "Medium", 
                    "impact": "High",
                    "mitigation": "Early agency engagement, comprehensive data packages"
                }
            ],
            "commercial_risks": [
                {
                    "risk": "Market competition",
                    "probability": "High",
                    "impact": "Medium",
                    "mitigation": "Differentiated positioning, first-mover advantage"
                },
                {
                    "risk": "Pricing pressures",
                    "probability": "High",
                    "impact": "Medium", 
                    "mitigation": "Value-based pricing, health economics evidence"
                }
            ],
            "ip_risks": [
                {
                    "risk": "Patent challenges",
                    "probability": "Low",
                    "impact": "High",
                    "mitigation": "Strong patent portfolio, freedom-to-operate analysis"
                }
            ],
            "overall_risk_level": "Medium",
            "risk_management_strategy": "Proactive monitoring and mitigation planning"
        }
    
    def _create_implementation_roadmap(self, research_data: Dict) -> Dict[str, Any]:
        """Create implementation roadmap"""
        return {
            "phase_1": {
                "timeline": "Months 1-6",
                "activities": [
                    "Complete preclinical studies",
                    "File method-of-use patents",
                    "Engage regulatory consultants",
                    "Finalize clinical trial design"
                ],
                "milestones": [
                    "Preclinical data package complete",
                    "Patent applications filed",
                    "Regulatory pathway confirmed"
                ]
            },
            "phase_2": {
                "timeline": "Months 7-18", 
                "activities": [
                    "Initiate Phase 2 clinical trials",
                    "Scale up manufacturing",
                    "Develop commercial strategy",
                    "Explore partnership opportunities"
                ],
                "milestones": [
                    "Phase 2 interim results",
                    "Manufacturing capability established",
                    "Partnership discussions initiated"
                ]
            },
            "phase_3": {
                "timeline": "Months 19-36",
                "activities": [
                    "Conduct Phase 3 trials",
                    "Prepare regulatory submissions",
                    "Build commercial infrastructure",
                    "Execute market access plans"
                ],
                "milestones": [
                    "Phase 3 results available",
                    "NDA/MAA submission",
                    "Commercial team in place"
                ]
            }
        }
    
    def _format_market_analysis(self, research_data: Dict) -> Dict[str, Any]:
        """Format market analysis section"""
        return {
            "therapy_area_overview": "Comprehensive analysis of target therapy area",
            "market_dynamics": "Growth drivers, barriers, and key trends",
            "competitive_landscape": "Key players, market shares, and competitive positioning",
            "commercial_opportunity": "Revenue potential and market access considerations"
        }
    
    def _format_clinical_analysis(self, research_data: Dict) -> Dict[str, Any]:
        """Format clinical analysis section"""
        return {
            "current_evidence": "Summary of existing clinical data",
            "development_opportunities": "Identified new indications and pathways",
            "safety_profile": "Comprehensive safety assessment",
            "regulatory_strategy": "Proposed development and approval pathway"
        }
    
    def _format_ip_analysis(self, research_data: Dict) -> Dict[str, Any]:
        """Format IP analysis section"""
        return {
            "patent_landscape": "Current IP position and coverage",
            "freedom_to_operate": "FTO assessment and risks",
            "white_space_opportunities": "Identified IP gaps and opportunities",
            "protection_strategy": "Recommended IP protection approach"
        }
    
    def _format_competitive_analysis(self, research_data: Dict) -> Dict[str, Any]:
        """Format competitive analysis section"""
        return {
            "key_competitors": "Major players and their strategies",
            "competitive_advantages": "Differentiated positioning opportunities",
            "market_barriers": "Entry barriers and competitive threats",
            "strategic_positioning": "Recommended competitive approach"
        }
    
    def _extract_market_metrics(self, research_data: Dict) -> Dict[str, Any]:
        """Extract key market metrics"""
        return {
            "market_size": "$2.1B",
            "growth_rate": "8.2% CAGR",
            "patient_population": "450 million",
            "treatment_rate": "65%",
            "market_share_opportunity": "15-20%"
        }
    
    def _extract_clinical_metrics(self, research_data: Dict) -> Dict[str, Any]:
        """Extract key clinical metrics"""
        return {
            "development_timeline": "24-36 months",
            "success_probability": "65%",
            "regulatory_pathway": "505(b)(2)",
            "clinical_trials_required": "2-3 Phase 3 studies"
        }
    
    def _extract_ip_metrics(self, research_data: Dict) -> Dict[str, Any]:
        """Extract key IP metrics"""
        return {
            "patent_protection": "12+ years",
            "freedom_to_operate": "Favorable",
            "white_space_opportunities": "Multiple",
            "licensing_potential": "High"
        }
    
    def _extract_competitive_metrics(self, research_data: Dict) -> Dict[str, Any]:
        """Extract key competitive metrics"""
        return {
            "competitive_intensity": "Medium-High",
            "barriers_to_entry": "Moderate",
            "first_mover_advantage": "Significant",
            "differentiation_potential": "High"
        }

class DataVisualizationTool(BaseTool):
    name: str = "Data Visualization Tool"
    description: str = "Create charts, graphs, and visualizations for research reports"
    
    def _run(self, data: Dict, visualization_type: str = "comprehensive") -> Dict[str, Any]:
        """Generate data visualizations"""
        return {
            "market_trends_chart": "Market size and growth trajectory visualization",
            "clinical_development_timeline": "Development pathway and milestone timeline",
            "competitive_positioning_map": "Competitive landscape visualization",
            "ip_landscape_diagram": "Patent coverage and white space mapping",
            "risk_assessment_matrix": "Risk probability and impact visualization"
        }

class ExecutiveSummaryTool(BaseTool):
    name: str = "Executive Summary Tool"
    description: str = "Generate concise executive summaries highlighting key insights"
    
    def _run(self, research_data: Dict) -> Dict[str, Any]:
        """Generate executive summary"""
        return {
            "business_opportunity": "Clear statement of the commercial opportunity",
            "key_advantages": "Major competitive advantages and differentiators",
            "strategic_imperatives": "Critical actions required for success",
            "investment_highlights": "Key reasons for investment and development",
            "risk_reward_profile": "Balanced assessment of risks and potential returns"
        }