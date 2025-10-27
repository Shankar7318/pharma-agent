import pandas as pd
import json
from typing import Dict, List, Any
from datetime import datetime

class DataProcessor:
    """Advanced data processing utilities for pharmaceutical research"""
    
    @staticmethod
    def format_market_analysis(data: Dict) -> pd.DataFrame:
        """Format market analysis data into structured DataFrame"""
        if not data:
            return pd.DataFrame()
        
        records = []
        if 'therapy_breakdown' in data:
            for therapy, metrics in data['therapy_breakdown'].items():
                records.append({
                    'therapy_area': therapy,
                    'market_share': metrics.get('market_share', 'N/A'),
                    'growth_rate': metrics.get('growth', 'N/A')
                })
        
        return pd.DataFrame(records)
    
    @staticmethod
    def format_clinical_trials(data: Dict) -> pd.DataFrame:
        """Format clinical trials data into structured DataFrame"""
        if not data or 'active_trials' not in data:
            return pd.DataFrame()
        
        trials_data = data['active_trials']
        df = pd.DataFrame(trials_data)
        
        # Add derived columns
        if not df.empty:
            if 'completion_date' in df.columns:
                df['completion_year'] = pd.to_datetime(df['completion_date'], errors='coerce').dt.year
            df['trial_duration'] = pd.to_datetime('2024-01-01')  # Mock calculation
        
        return df
    
    @staticmethod
    def format_patent_data(data: Dict) -> pd.DataFrame:
        """Format patent data into structured DataFrame"""
        if not data or 'patents' not in data:
            return pd.DataFrame()
        
        patents_data = data['patents']
        df = pd.DataFrame(patents_data)
        
        if not df.empty and 'filing_date' in df.columns:
            df['filing_year'] = pd.to_datetime(df['filing_date'], errors='coerce').dt.year
            if 'expiry_date' in df.columns:
                df['years_remaining'] = pd.to_datetime(df['expiry_date'], errors='coerce').dt.year - datetime.now().year
        
        return df
    
    @staticmethod
    def calculate_research_metrics(research_results: Dict[str, Any]) -> Dict[str, float]:
        """Calculate comprehensive research metrics"""
        metrics = {
            'research_completeness': 0.0,
            'confidence_score': 0.0,
            'data_quality_score': 0.0,
            'total_data_points': 0
        }
        
        # Calculate completeness based on available data modules
        available_modules = len([v for v in research_results.values() if v])
        metrics['research_completeness'] = (available_modules / 5) * 100  # 5 main modules
        
        # Calculate confidence score based on data quality
        if research_results.get('market_data'):
            metrics['confidence_score'] += 20
        if research_results.get('trials_data'):
            metrics['confidence_score'] += 25
        if research_results.get('patent_data'):
            metrics['confidence_score'] += 25
        if research_results.get('trade_data'):
            metrics['confidence_score'] += 15
        if research_results.get('repurposing_analysis'):
            metrics['confidence_score'] += 15
        
        # Data quality score (simplified)
        metrics['data_quality_score'] = min(metrics['confidence_score'] * 1.1, 100)
        
        # Total data points
        metrics['total_data_points'] = sum([
            len(research_results.get('market_data', {})),
            len(research_results.get('trials_data', {}).get('active_trials', [])),
            len(research_results.get('patent_data', {}).get('patents', [])),
            len(research_results.get('trade_data', {}).get('export_data', [])),
            len(research_results.get('repurposing_analysis', {}))
        ])
        
        return metrics
    
    @staticmethod
    def generate_comparative_analysis(molecules: List[str], therapy_area: str) -> Dict[str, Any]:
        """Generate comparative analysis between multiple molecules"""
        analysis = {
            'therapy_area': therapy_area,
            'molecules_compared': molecules,
            'comparative_metrics': {},
            'recommendations': []
        }
        
        # Mock comparative metrics
        for molecule in molecules:
            analysis['comparative_metrics'][molecule] = {
                'repurposing_potential': ['High', 'Medium', 'Low'][hash(molecule) % 3],
                'development_timeline': f"{2 + (hash(molecule) % 4)}-{4 + (hash(molecule) % 4)} years",
                'estimated_cost': f"${50 + (hash(molecule) % 100)}-{150 + (hash(molecule) % 200)}M",
                'commercial_potential': ['High', 'Medium', 'Low'][(hash(molecule) + 1) % 3]
            }
        
        # Generate recommendations
        analysis['recommendations'] = [
            f"Prioritize {molecules[0]} for initial development based on highest repurposing potential",
            "Consider combination therapies for enhanced efficacy",
            "Conduct additional preclinical validation for all candidates"
        ]
        
        return analysis
    
    @staticmethod
    def validate_research_data(data: Dict) -> Dict[str, Any]:
        """Validate research data for completeness and quality"""
        validation_results = {
            'is_valid': True,
            'missing_fields': [],
            'data_quality_issues': [],
            'recommendations': []
        }
        
        required_fields = ['molecule', 'therapy_area', 'research_goal']
        for field in required_fields:
            if field not in data or not data[field]:
                validation_results['missing_fields'].append(field)
                validation_results['is_valid'] = False
        
        # Check data quality
        if 'market_data' in data and not data['market_data']:
            validation_results['data_quality_issues'].append('Market data is empty')
        
        if 'trials_data' in data and data['trials_data'].get('total_trials', 0) == 0:
            validation_results['data_quality_issues'].append('No clinical trials data available')
        
        # Generate recommendations
        if validation_results['missing_fields']:
            validation_results['recommendations'].append(
                f"Please provide: {', '.join(validation_results['missing_fields'])}"
            )
        
        if validation_results['data_quality_issues']:
            validation_results['recommendations'].append(
                "Consider enhancing data quality for more accurate analysis"
            )
        
        return validation_results


class ReportGenerator:
    """Advanced report generation utilities"""
    
    @staticmethod
    def generate_executive_summary(research_data: Dict) -> str:
        """Generate comprehensive executive summary from research data"""
        molecule = research_data.get('molecule', 'Unknown')
        therapy_area = research_data.get('therapy_area', 'Unknown')
        research_goal = research_data.get('research_goal', 'General analysis')
        
        metrics = DataProcessor.calculate_research_metrics(research_data.get('results', {}))
        
        summary = f"""
PHARMACEUTICAL RESEARCH EXECUTIVE SUMMARY
==========================================

RESEARCH OVERVIEW
-----------------
Molecule: {molecule.upper()}
Therapy Area: {therapy_area.upper()}
Research Goal: {research_goal}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

RESEARCH METRICS
----------------
• Data Completeness: {metrics['research_completeness']:.1f}%
• Confidence Score: {metrics['confidence_score']:.1f}%
• Data Quality: {metrics['data_quality_score']:.1f}%

KEY FINDINGS
------------
1. Market Opportunity: Significant growth potential identified in target therapy area
2. Clinical Development: Multiple repurposing pathways available
3. Intellectual Property: Favorable landscape with strategic opportunities
4. Commercial Viability: Strong potential for successful development

STRATEGIC RECOMMENDATIONS
-------------------------
1. Pursue 505(b)(2) regulatory pathway for expedited approval
2. Develop comprehensive IP protection strategy
3. Initiate preclinical validation studies
4. Explore partnership opportunities for development

NEXT STEPS
----------
• Conduct detailed feasibility assessment
• Engage regulatory consultants
• Develop project timeline and budget
• Identify potential development partners

---
Generated by Pharmaceutical Agentic AI Research Platform
Confidential - For Internal Use Only
"""
        return summary
    
    @staticmethod
    def generate_detailed_analysis(research_data: Dict) -> Dict[str, Any]:
        """Generate detailed analysis report"""
        analysis = {
            'executive_summary': ReportGenerator.generate_executive_summary(research_data),
            'market_analysis': ReportGenerator._format_market_section(research_data.get('results', {}).get('market_data', {})),
            'clinical_analysis': ReportGenerator._format_clinical_section(research_data.get('results', {}).get('trials_data', {})),
            'ip_analysis': ReportGenerator._format_ip_section(research_data.get('results', {}).get('patent_data', {})),
            'commercial_recommendations': ReportGenerator._generate_commercial_recommendations(research_data)
        }
        
        return analysis
    
    @staticmethod
    def generate_pdf_report(research_data: Dict, filename: str = None) -> Dict[str, Any]:
        """Generate PDF report (mock implementation)"""
        if filename is None:
            filename = f"pharma_research_report_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
        
        detailed_analysis = ReportGenerator.generate_detailed_analysis(research_data)
        report_content = detailed_analysis['executive_summary']
        
        # Add detailed sections
        for section_name, section_content in detailed_analysis.items():
            if section_name != 'executive_summary':
                report_content += f"\n\n{section_name.upper()}\n{'-'*40}\n{section_content}"
        
        return {
            'filename': filename,
            'content': report_content,
            'format': 'text',
            'sections': list(detailed_analysis.keys()),
            'generation_time': datetime.now().isoformat()
        }
    
    @staticmethod
    def _format_market_section(market_data: Dict) -> str:
        """Format market analysis section"""
        if not market_data:
            return "No market data available for analysis."
        
        return f"""
Market Size: {market_data.get('market_size', 'N/A')}
Growth Rate (CAGR): {market_data.get('cagr', 'N/A')}
Key Players: {', '.join(market_data.get('key_players', []))}
Competitive Landscape: {market_data.get('competitors', 'N/A')} competitors

Growth Drivers:
{chr(10).join(f"• {driver}" for driver in market_data.get('growth_drivers', []))}
"""
    
    @staticmethod
    def _format_clinical_section(trials_data: Dict) -> str:
        """Format clinical analysis section"""
        if not trials_data or trials_data.get('total_trials', 0) == 0:
            return "No clinical trials data available for analysis."
        
        return f"""
Total Clinical Trials: {trials_data.get('total_trials', 0)}
Active Trials: {len(trials_data.get('active_trials', []))}
Repurposing Opportunities: {len(trials_data.get('repurposing_opportunities', []))}

Summary: {trials_data.get('summary', 'No summary available')}
"""
    
    @staticmethod
    def _format_ip_section(patent_data: Dict) -> str:
        """Format IP analysis section"""
        if not patent_data or patent_data.get('total_patents', 0) == 0:
            return "No patent data available for analysis."
        
        return f"""
Total Patents: {patent_data.get('total_patents', 0)}
Freedom to Operate: {patent_data.get('freedom_to_operate', 'Unknown')}

Key Recommendations:
{chr(10).join(f"• {rec}" for rec in patent_data.get('recommendations', []))}
"""
    
    @staticmethod
    def _generate_commercial_recommendations(research_data: Dict) -> str:
        """Generate commercial recommendations"""
        molecule = research_data.get('molecule', 'the molecule')
        
        return f"""
COMMERCIAL STRATEGY FOR {molecule.upper()}

1. DEVELOPMENT STRATEGY
   • Pursue 505(b)(2) regulatory pathway
   • Target 24-36 month development timeline
   • Budget: $50-100M for complete development

2. MARKET ACCESS
   • Develop value-based pricing strategy
   • Engage payers early in development
   • Generate robust health economics evidence

3. COMMERCIALIZATION
   • Target specialist physicians initially
   • Develop patient support programs
   • Consider co-promotion partnerships

4. RISK MITIGATION
   • Conduct thorough FTO analysis
   • Implement phase-gated development
   • Maintain regulatory flexibility
"""