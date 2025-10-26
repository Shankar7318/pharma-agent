from crewai import Agent
from crewai_tools import BaseTool
import json
from typing import Dict, List, Any

class PatentLandscapeAgent(Agent):
    """Specialized agent for pharmaceutical intellectual property analysis"""
    
    def __init__(self):
        super().__init__(
            role="Pharmaceutical Intellectual Property Strategist",
            goal="Analyze patent landscapes, identify IP opportunities, and assess freedom-to-operate for drug repurposing",
            backstory="""You are a pharmaceutical patent expert with extensive 
            experience in IP strategy, freedom-to-operate analysis, patent lifecycle 
            management, and competitive intelligence.
            
            Your capabilities include:
            - Patent landscape mapping and analysis
            - Freedom-to-operate assessment
            - White space opportunity identification
            - Competitive IP intelligence
            - Licensing and partnership evaluation""",
            tools=[PatentAnalysisTool(), FTOTool(), IPStrategyTool()],
            verbose=True
        )

class PatentAnalysisTool(BaseTool):
    name: str = "Patent Analysis Tool"
    description: str = "Comprehensive analysis of pharmaceutical patent landscapes and IP opportunities"
    
    def _run(self, molecule: str, analysis_type: str = "comprehensive") -> Dict[str, Any]:
        """Conduct comprehensive patent analysis for pharmaceutical molecule"""
        try:
            with open('data/patents.json', 'r') as f:
                patents_data = json.load(f)
            
            with open('data/molecules.json', 'r') as f:
                molecules_data = json.load(f)
            
            molecule_patents = self._get_molecule_patents(patents_data, molecule)
            molecule_info = self._get_molecule_info(molecules_data, molecule)
            
            return {
                "molecule": molecule_info,
                "patent_landscape": self._analyze_patent_landscape(molecule_patents),
                "freedom_to_operate": self._assess_fto(molecule_patents),
                "competitive_ip": self._analyze_competitive_ip(molecule_patents),
                "strategic_recommendations": self._generate_ip_recommendations(molecule_patents, molecule_info)
            }
            
        except Exception as e:
            return {"error": f"Patent analysis failed: {str(e)}"}
    
    def _get_molecule_patents(self, patents_data: Dict, molecule: str) -> List[Dict]:
        """Get all patents for specific molecule"""
        return [patent for patent in patents_data.get('pharmaceutical_patents', []) 
                if patent.get('molecule', '').lower() == molecule.lower()]
    
    def _get_molecule_info(self, molecules_data: Dict, molecule: str) -> Dict:
        """Get molecule information"""
        for mol in molecules_data.get('pharmaceutical_molecules', []):
            if mol.get('generic_name', '').lower() == molecule.lower():
                return mol
        return {}
    
    def _analyze_patent_landscape(self, patents: List[Dict]) -> Dict[str, Any]:
        """Analyze comprehensive patent landscape"""
        if not patents:
            return {"status": "No patents found", "opportunity": "High"}
        
        active_patents = [p for p in patents if p.get('legal_status') == 'Active']
        pending_patents = [p for p in patents if p.get('legal_status') == 'Pending']
        
        return {
            "total_patents": len(patents),
            "active_patents": len(active_patents),
            "pending_patents": len(pending_patents),
            "patent_types": self._categorize_patent_types(patents),
            "jurisdiction_coverage": self._analyze_jurisdiction_coverage(patents),
            "key_assignees": self._identify_key_assignees(patents),
            "patent_quality": self._assess_patent_quality(patents),
            "timeline_analysis": self._analyze_patent_timeline(patents)
        }
    
    def _assess_fto(self, patents: List[Dict]) -> Dict[str, Any]:
        """Assess freedom-to-operate landscape"""
        if not patents:
            return {"status": "Favorable", "risk_level": "Low", "reasoning": "No blocking patents identified"}
        
        # Analyze FTO from patent data
        fto_risks = []
        blocking_patents = []
        
        for patent in patents:
            fto_analysis = patent.get('freedom_to_operate_analysis', {})
            if fto_analysis.get('infringement_risk') in ['High', 'Medium']:
                blocking_patents.append({
                    'patent_number': patent.get('patent_number'),
                    'risk_level': fto_analysis.get('infringement_risk'),
                    'reason': fto_analysis.get('blocking_patents', [])
                })
        
        overall_risk = "High" if any(p['risk_level'] == 'High' for p in blocking_patents) else "Medium" if blocking_patents else "Low"
        
        return {
            "status": "Favorable" if overall_risk == "Low" else "Challenging",
            "risk_level": overall_risk,
            "blocking_patents": blocking_patents,
            "recommendations": self._generate_fto_recommendations(blocking_patents)
        }
    
    def _analyze_competitive_ip(self, patents: List[Dict]) -> Dict[str, Any]:
        """Analyze competitive IP positioning"""
        assignee_analysis = {}
        for patent in patents:
            assignee = patent.get('assignee')
            if assignee not in assignee_analysis:
                assignee_analysis[assignee] = {
                    'patent_count': 0,
                    'avg_citations': 0,
                    'patent_types': set(),
                    'jurisdictions': set()
                }
            
            assignee_analysis[assignee]['patent_count'] += 1
            assignee_analysis[assignee]['avg_citations'] += patent.get('citation_count', 0)
            assignee_analysis[assignee]['patent_types'].add(patent.get('patent_type'))
            assignee_analysis[assignee]['jurisdictions'].update(patent.get('jurisdictions', []))
        
        # Convert sets to lists for JSON serialization
        for assignee in assignee_analysis:
            assignee_analysis[assignee]['patent_types'] = list(assignee_analysis[assignee]['patent_types'])
            assignee_analysis[assignee]['jurisdictions'] = list(assignee_analysis[assignee]['jurisdictions'])
            if assignee_analysis[assignee]['patent_count'] > 0:
                assignee_analysis[assignee]['avg_citations'] /= assignee_analysis[assignee]['patent_count']
        
        return {
            "key_players": assignee_analysis,
            "ip_competitiveness": self._assess_ip_competitiveness(assignee_analysis),
            "licensing_opportunities": self._identify_licensing_opportunities(patents)
        }
    
    def _generate_ip_recommendations(self, patents: List[Dict], molecule_info: Dict) -> List[Dict]:
        """Generate strategic IP recommendations"""
        recommendations = []
        
        if not patents:
            recommendations.append({
                "type": "IP Protection",
                "priority": "High",
                "recommendation": "File method-of-use patents for new indications",
                "rationale": "No existing patent protection identified"
            })
        else:
            # Analyze existing patents and identify gaps
            patent_types = set(p.get('patent_type') for p in patents)
            
            if 'Formulation' not in patent_types:
                recommendations.append({
                    "type": "Formulation IP",
                    "priority": "Medium",
                    "recommendation": "Develop and patent novel formulations",
                    "rationale": "Gap in formulation patent coverage"
                })
            
            if 'Method-of-use' not in patent_types:
                recommendations.append({
                    "type": "Method-of-use",
                    "priority": "High", 
                    "recommendation": "File patents for new therapeutic uses",
                    "rationale": "Core opportunity for drug repurposing"
                })
        
        # Add strategic recommendations based on molecule characteristics
        repurposing_potential = molecule_info.get('repurposing_potential', 'Medium')
        if repurposing_potential in ['High', 'Very High']:
            recommendations.append({
                "type": "Strategic IP",
                "priority": "High",
                "recommendation": "Build comprehensive IP portfolio around new indications",
                "rationale": f"High repurposing potential ({repurposing_potential}) identified"
            })
        
        return recommendations
    
    def _categorize_patent_types(self, patents: List[Dict]) -> Dict[str, int]:
        """Categorize patents by type"""
        types = {}
        for patent in patents:
            p_type = patent.get('patent_type', 'Unknown')
            types[p_type] = types.get(p_type, 0) + 1
        return types
    
    def _analyze_jurisdiction_coverage(self, patents: List[Dict]) -> Dict[str, int]:
        """Analyze patent jurisdiction coverage"""
        jurisdictions = {}
        for patent in patents:
            for jurisdiction in patent.get('jurisdictions', []):
                jurisdictions[jurisdiction] = jurisdictions.get(jurisdiction, 0) + 1
        return jurisdictions
    
    def _identify_key_assignees(self, patents: List[Dict]) -> List[Dict]:
        """Identify key patent assignees"""
        assignees = {}
        for patent in patents:
            assignee = patent.get('assignee')
            if assignee not in assignees:
                assignees[assignee] = {
                    'patent_count': 0,
                    'avg_claims': 0,
                    'total_citations': 0
                }
            assignees[assignee]['patent_count'] += 1
            assignees[assignee]['avg_claims'] += patent.get('claims_count', 0)
            assignees[assignee]['total_citations'] += patent.get('citation_count', 0)
        
        # Calculate averages
        for assignee in assignees:
            if assignees[assignee]['patent_count'] > 0:
                assignees[assignee]['avg_claims'] /= assignees[assignee]['patent_count']
        
        return [{'assignee': k, **v} for k, v in assignees.items()]
    
    def _assess_patent_quality(self, patents: List[Dict]) -> Dict[str, Any]:
        """Assess overall patent quality"""
        if not patents:
            return {"score": 0, "assessment": "No patents available"}
        
        avg_claims = sum(p.get('claims_count', 0) for p in patents) / len(patents)
        avg_citations = sum(p.get('citation_count', 0) for p in patents) / len(patents)
        active_ratio = len([p for p in patents if p.get('legal_status') == 'Active']) / len(patents)
        
        quality_score = (avg_claims * 0.3) + (avg_citations * 0.4) + (active_ratio * 0.3)
        
        return {
            "score": round(quality_score, 2),
            "assessment": "High" if quality_score > 50 else "Medium" if quality_score > 25 else "Low",
            "metrics": {
                "average_claims": round(avg_claims, 1),
                "average_citations": round(avg_citations, 1),
                "active_patent_ratio": round(active_ratio, 2)
            }
        }
    
    def _analyze_patent_timeline(self, patents: List[Dict]) -> Dict[str, Any]:
        """Analyze patent timeline and expiry patterns"""
        if not patents:
            return {"earliest_expiry": None, "latest_expiry": None, "coverage_gap": "No patents"}
        
        expiry_dates = [p.get('expiry_date') for p in patents if p.get('expiry_date')]
        if expiry_dates:
            earliest = min(expiry_dates)
            latest = max(expiry_dates)
            return {
                "earliest_expiry": earliest,
                "latest_expiry": latest,
                "coverage_gap": "Continuous" if len(expiry_dates) > 3 else "Potential gaps",
                "strategic_implications": self._derive_timeline_implications(earliest, latest)
            }
        return {"earliest_expiry": None, "latest_expiry": None, "coverage_gap": "Unknown"}
    
    def _derive_timeline_implications(self, earliest: str, latest: str) -> List[str]:
        """Derive strategic implications from patent timeline"""
        implications = []
        # Add timeline analysis logic
        return implications
    
    def _generate_fto_recommendations(self, blocking_patents: List[Dict]) -> List[str]:
        """Generate FTO recommendations"""
        recommendations = []
        if blocking_patents:
            recommendations.extend([
                "Conduct detailed FTO analysis with patent counsel",
                "Consider design-around strategies for key patents",
                "Explore licensing opportunities for blocking IP",
                "Evaluate patent invalidation possibilities"
            ])
        else:
            recommendations.append("FTO appears favorable for development")
        
        return recommendations
    
    def _assess_ip_competitiveness(self, assignee_analysis: Dict) -> str:
        """Assess overall IP competitiveness"""
        if not assignee_analysis:
            return "Open Field"
        
        player_count = len(assignee_analysis)
        avg_patents = sum(data['patent_count'] for data in assignee_analysis.values()) / player_count
        
        if avg_patents > 10:
            return "Highly Competitive"
        elif avg_patents > 5:
            return "Moderately Competitive"
        else:
            return "Emerging Competition"
    
    def _identify_licensing_opportunities(self, patents: List[Dict]) -> List[Dict]:
        """Identify potential licensing opportunities"""
        opportunities = []
        for patent in patents:
            if patent.get('licensing_availability'):
                opportunities.append({
                    'patent_number': patent.get('patent_number'),
                    'assignee': patent.get('assignee'),
                    'estimated_royalty': patent.get('estimated_royalty_rate'),
                    'potential_value': 'High' if patent.get('commercial_potential') in ['High', 'Very High'] else 'Medium'
                })
        return opportunities