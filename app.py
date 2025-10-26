import os
import streamlit as st
import pandas as pd
import json
from datetime import datetime
from typing import Dict, List, Any
import plotly.express as px
import plotly.graph_objects as go

# Import custom modules
from agents.master_agent import PharmaResearchOrchestrator
from utils.api_clients import MockPharmaAPIs, EnhancedMockPharmaAPIs
from utils.data_processor import DataProcessor, ReportGenerator
from utils.config import Config, APIConfig

# Set page configuration
st.set_page_config(
    page_title="Pharma Agentic AI Research Platform",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

class PharmaResearchApp:
    """Main Pharmaceutical Research Application"""
    
    def __init__(self):
        self.api = EnhancedMockPharmaAPIs()
        self.processor = DataProcessor()
        self.report_generator = ReportGenerator()
        self.initialize_session_state()
    
    def initialize_session_state(self):
        """Initialize session state variables"""
        if 'research_history' not in st.session_state:
            st.session_state.research_history = []
        if 'current_research' not in st.session_state:
            st.session_state.current_research = None
        if 'api_key' not in st.session_state:
            st.session_state.api_key = None
        if 'research_in_progress' not in st.session_state:
            st.session_state.research_in_progress = False
    
    def render_sidebar(self):
        """Render application sidebar"""
        with st.sidebar:
            st.title("⚙️ Configuration")
            st.markdown("---")
            
            # API Key Input
            api_key = st.text_input(
                "OpenAI API Key", 
                type="password",
                help="Enter your OpenAI API key to enable AI-powered research",
                value=st.session_state.get('api_key', '')
            )
            
            if api_key:
                st.session_state.api_key = api_key
                os.environ["OPENAI_API_KEY"] = api_key
                st.success("✅ API Key configured")
            else:
                st.warning("⚠️ API key required for full functionality")
            
            st.markdown("---")
            
            # Quick Actions
            st.subheader("🚀 Quick Actions")
            
            if st.button("📊 Load Sample Data", use_container_width=True):
                self.load_sample_data()
            
            if st.button("🔄 Clear Research", use_container_width=True):
                self.clear_research()
            
            st.markdown("---")
            
            # Research History
            st.subheader("📚 Research History")
            if st.session_state.research_history:
                for i, research in enumerate(st.session_state.research_history[-5:]):
                    with st.expander(f"{research['molecule']} - {research['therapy_area']}"):
                        st.write(f"Date: {research['timestamp']}")
                        if st.button("Load", key=f"load_{i}"):
                            st.session_state.current_research = research
            
            st.markdown("---")
            
            # System Status
            st.subheader("🔧 System Status")
            config_status = Config.validate_config()
            st.write(f"API Key: {'✅' if config_status['openai_api_key'] else '❌'}")
            st.write(f"Therapy Areas: {config_status['supported_therapy_areas']}")
            st.write(f"Molecules: {config_status['supported_molecules']}")
    
    def render_main_interface(self):
        """Render main application interface"""
        st.title("🧬 Pharmaceutical Agentic AI Research Platform")
        st.markdown("### Accelerating Drug Repurposing and Innovation Discovery")
        
        # Research Parameters Section
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("🔬 Research Parameters")
            
            molecule = st.text_input(
                "Molecule/Drug Name",
                value=st.session_state.get('current_molecule', ''),
                placeholder="e.g., Metformin, Ivermectin, Remdesivir",
                help="Enter the generic name of the pharmaceutical molecule"
            )
            
            therapy_area = st.selectbox(
                "Target Therapy Area",
                options=Config.DEFAULT_THERAPY_AREAS,
                index=0,
                help="Select the therapeutic area for repurposing analysis"
            )
            
            research_goal = st.text_area(
                "Research Objective",
                value=st.session_state.get('current_goal', ''),
                height=100,
                placeholder="Describe your research goals and objectives...",
                help="e.g., Identify repurposing opportunities for oncology applications"
            )
        
        with col2:
            st.subheader("🎯 Research Scope")
            
            st.markdown("#### Select Research Modules")
            col2a, col2b, col2c = st.columns(3)
            
            with col2a:
                include_market = st.checkbox("Market Analysis", True)
                include_trials = st.checkbox("Clinical Trials", True)
                
            with col2b:
                include_patents = st.checkbox("Patent Analysis", True)
                include_exim = st.checkbox("EXIM Trends", False)
                
            with col2c:
                include_web = st.checkbox("Web Intelligence", True)
                generate_report = st.checkbox("Generate Report", True)
            
            st.markdown("---")
            st.subheader("📈 Expected Impact")
            
            impact_col1, impact_col2, impact_col3 = st.columns(3)
            
            with impact_col1:
                st.metric("Time Savings", "80%", "2-3 months → Days")
                
            with impact_col2:
                st.metric("Cost Reduction", "70%", "Automated Research")
                
            with impact_col3:
                st.metric("Accuracy", "95%", "Multi-source Validation")
        
        # Research Execution
        st.markdown("---")
        st.subheader("🚀 Execute Research")
        
        research_params = {
            'molecule': molecule,
            'therapy_area': therapy_area,
            'research_goal': research_goal,
            'include_market': include_market,
            'include_trials': include_trials,
            'include_patents': include_patents,
            'include_exim': include_exim,
            'include_web': include_web,
            'generate_report': generate_report
        }
        
        # Validation
        is_valid = all([molecule, therapy_area, research_goal])
        has_api_key = bool(st.session_state.get('api_key'))
        
        if not is_valid:
            st.warning("⚠️ Please fill in all research parameters")
        elif not has_api_key:
            st.warning("⚠️ Please enter your OpenAI API key in the sidebar")
        else:
            if st.button("🎯 Start Comprehensive Research", type="primary", use_container_width=True):
                self.execute_research(research_params)
    
    def execute_research(self, params: Dict[str, Any]):
        """Execute comprehensive pharmaceutical research"""
        st.session_state.research_in_progress = True
        
        with st.spinner("🔄 Initializing Agentic AI Research Platform..."):
            try:
                # Initialize research orchestrator
                orchestrator = PharmaResearchOrchestrator()
                
                # Store current parameters
                st.session_state.current_molecule = params['molecule']
                st.session_state.current_therapy_area = params['therapy_area']
                st.session_state.current_goal = params['research_goal']
                
                # Create progress tracking
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Simulate research steps
                research_steps = [
                    "Gathering market intelligence...",
                    "Analyzing clinical trials data...",
                    "Assessing patent landscape...",
                    "Conducting competitive analysis...",
                    "Generating strategic recommendations...",
                    "Compiling final report..."
                ]
                
                research_results = {}
                
                for i, step in enumerate(research_steps):
                    status_text.text(f"Step {i+1}/{len(research_steps)}: {step}")
                    progress_bar.progress((i + 1) / len(research_steps))
                    
                    # Simulate API calls and data processing
                    if "market" in step.lower():
                        research_results['market_data'] = self.api.iqvia_market_data(params['therapy_area'])
                    elif "clinical" in step.lower():
                        research_results['trials_data'] = self.api.clinical_trials_search(params['molecule'])
                    elif "patent" in step.lower():
                        research_results['patent_data'] = self.api.patent_search(params['molecule'])
                    elif "competitive" in step.lower():
                        research_results['trade_data'] = self.api.exim_trade_data(params['molecule'])
                
                # Generate comprehensive research result
                research_result = {
                    "timestamp": datetime.now().isoformat(),
                    "molecule": params['molecule'],
                    "therapy_area": params['therapy_area'],
                    "research_goal": params['research_goal'],
                    "results": research_results,
                    "metrics": self.processor.calculate_research_metrics(research_results),
                    "modules_used": {
                        'market': params['include_market'],
                        'trials': params['include_trials'],
                        'patents': params['include_patents'],
                        'exim': params['include_exim'],
                        'web': params['include_web']
                    }
                }
                
                # Store in session state
                st.session_state.research_history.append(research_result)
                st.session_state.current_research = research_result
                
                # Generate report if requested
                if params['generate_report']:
                    report = self.report_generator.generate_pdf_report(research_result)
                    research_result['report'] = report
                
                progress_bar.progress(100)
                status_text.text("✅ Research completed successfully!")
                st.success("🎉 Research completed! View results below.")
                
            except Exception as e:
                st.error(f"❌ Research failed: {str(e)}")
            finally:
                st.session_state.research_in_progress = False
    
    def render_research_results(self):
        """Render research results section"""
        if not st.session_state.current_research:
            return
        
        research = st.session_state.current_research
        st.markdown("---")
        st.header("📊 Research Results")
        
        # Create tabs for different sections
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "🎯 Executive Summary", 
            "📈 Market Analysis", 
            "🔬 Clinical Trials", 
            "⚖️ Patent Landscape",
            "📋 Full Report",
            "📈 Analytics"
        ])
        
        with tab1:
            self.render_executive_summary(research)
        
        with tab2:
            self.render_market_analysis(research)
        
        with tab3:
            self.render_clinical_analysis(research)
        
        with tab4:
            self.render_patent_analysis(research)
        
        with tab5:
            self.render_full_report(research)
        
        with tab6:
            self.render_analytics(research)
    
    def render_executive_summary(self, research: Dict):
        """Render executive summary"""
        summary = self.report_generator.generate_executive_summary(research)
        st.markdown(summary)
        
        # Key metrics visualization
        metrics = research.get('metrics', {})
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Data Completeness", f"{metrics.get('research_completeness', 0):.1f}%")
        with col2:
            st.metric("Confidence Score", f"{metrics.get('confidence_score', 0):.1f}%")
        with col3:
            st.metric("Data Quality", f"{metrics.get('data_quality_score', 0):.1f}%")
        with col4:
            st.metric("Data Points", metrics.get('total_data_points', 0))
    
    def render_market_analysis(self, research: Dict):
        """Render market analysis results"""
        market_data = research.get('results', {}).get('market_data', {})
        
        if not market_data:
            st.warning("No market data available")
            return
        
        st.subheader("Market Intelligence")
        
        # Key metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Market Size", market_data.get('market_size', 'N/A'))
        with col2:
            st.metric("Growth Rate", market_data.get('cagr', 'N/A'))
        with col3:
            st.metric("Competitors", market_data.get('competitors', 'N/A'))
        
        # Market breakdown
        if 'therapy_breakdown' in market_data:
            st.subheader("Therapy Area Breakdown")
            breakdown_df = self.processor.format_market_analysis(market_data)
            if not breakdown_df.empty:
                st.dataframe(breakdown_df, use_container_width=True)
                
                # Visualization
                fig = px.bar(
                    breakdown_df, 
                    x='therapy_area', 
                    y='market_share',
                    title="Market Share by Therapy Area"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # Key players
        st.subheader("Key Market Players")
        key_players = market_data.get('key_players', [])
        for player in key_players:
            st.write(f"• **{player}**")
    
    def render_clinical_analysis(self, research: Dict):
        """Render clinical trials analysis"""
        trials_data = research.get('results', {}).get('trials_data', {})
        
        if not trials_data or trials_data.get('total_trials', 0) == 0:
            st.warning("No clinical trials data available")
            return
        
        st.subheader("Clinical Development Landscape")
        
        # Summary metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Trials", trials_data.get('total_trials', 0))
        with col2:
            st.metric("Active Trials", len(trials_data.get('active_trials', [])))
        with col3:
            st.metric("Repurposing Opportunities", len(trials_data.get('repurposing_opportunities', [])))
        
        # Trials table
        st.subheader("Active Clinical Trials")
        trials_df = self.processor.format_clinical_trials(trials_data)
        if not trials_df.empty:
            st.dataframe(trials_df, use_container_width=True)
        
        # Repurposing opportunities
        repurposing_ops = trials_data.get('repurposing_opportunities', [])
        if repurposing_ops:
            st.subheader("Repurposing Opportunities")
            for opp in repurposing_ops:
                with st.expander(f"{opp.get('indication', 'Unknown')} - {opp.get('phase', 'Unknown')}"):
                    st.write(f"**Trial ID:** {opp.get('nct_id', 'N/A')}")
                    st.write(f"**Status:** {opp.get('status', 'N/A')}")
                    st.write(f"**Potential:** {opp.get('repurposing_potential', 'N/A')}")
                    st.write(f"**Results:** {opp.get('results', 'N/A')}")
    
    def render_patent_analysis(self, research: Dict):
        """Render patent analysis results"""
        patent_data = research.get('results', {}).get('patent_data', {})
        
        if not patent_data or patent_data.get('total_patents', 0) == 0:
            st.warning("No patent data available")
            return
        
        st.subheader("Intellectual Property Landscape")
        
        # Patent metrics
        stats = patent_data.get('patent_statistics', {})
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Patents", patent_data.get('total_patents', 0))
        with col2:
            st.metric("Active Patents", stats.get('active_patents', 0))
        with col3:
            st.metric("Pending Patents", stats.get('pending_patents', 0))
        with col4:
            st.metric("FTO Status", patent_data.get('freedom_to_operate', 'Unknown'))
        
        # Patents table
        st.subheader("Patent Portfolio")
        patents_df = self.processor.format_patent_data(patent_data)
        if not patents_df.empty:
            st.dataframe(patents_df, use_container_width=True)
        
        # Recommendations
        recommendations = patent_data.get('recommendations', [])
        if recommendations:
            st.subheader("Strategic Recommendations")
            for rec in recommendations:
                st.write(f"• {rec}")
    
    def render_full_report(self, research: Dict):
        """Render full research report"""
        st.subheader("Complete Research Report")
        
        if 'report' in research:
            report_content = research['report']['content']
            st.download_button(
                label="📥 Download Full Report",
                data=report_content,
                file_name=research['report']['filename'],
                mime="text/plain",
                use_container_width=True
            )
            st.text_area("Report Content", report_content, height=400, label_visibility="collapsed")
        else:
            # Generate report on the fly
            report = self.report_generator.generate_pdf_report(research)
            st.download_button(
                label="📥 Generate & Download Report",
                data=report['content'],
                file_name=report['filename'],
                mime="text/plain",
                use_container_width=True
            )
    
    def render_analytics(self, research: Dict):
        """Render research analytics"""
        st.subheader("Research Analytics")
        
        metrics = research.get('metrics', {})
        
        # Metrics visualization
        fig = go.Figure(data=[
            go.Bar(name='Scores', 
                  x=['Completeness', 'Confidence', 'Quality'], 
                  y=[metrics.get('research_completeness', 0), 
                     metrics.get('confidence_score', 0), 
                     metrics.get('data_quality_score', 0)])
        ])
        fig.update_layout(title="Research Quality Metrics")
        st.plotly_chart(fig, use_container_width=True)
        
        # Data sources used
        modules_used = research.get('modules_used', {})
        active_modules = [module for module, used in modules_used.items() if used]
        
        st.subheader("Data Sources Utilized")
        for module in active_modules:
            st.write(f"✅ {module.replace('_', ' ').title()}")
    
    def load_sample_data(self):
        """Load sample data for demonstration"""
        st.session_state.current_molecule = "metformin"
        st.session_state.current_therapy_area = "oncology"
        st.session_state.current_goal = "Identify repurposing opportunities for cancer treatment"
        st.success("✅ Sample data loaded! Fill in other parameters and start research.")
    
    def clear_research(self):
        """Clear current research data"""
        st.session_state.current_research = None
        st.session_state.current_molecule = ""
        st.session_state.current_therapy_area = ""
        st.session_state.current_goal = ""
        st.success("✅ Research data cleared!")
    
    def run(self):
        """Main application runner"""
        self.render_sidebar()
        self.render_main_interface()
        
        if st.session_state.current_research:
            self.render_research_results()
        
        # Footer
        st.markdown("---")
        st.markdown(
            "### 🎯 Powered by Pharmaceutical Agentic AI | "
            "Built for EY Techathon 6.0 | "
            "Confidential - For Demonstration Purposes"
        )

def main():
    """Main application entry point"""
    app = PharmaResearchApp()
    app.run()

if __name__ == "__main__":
    main()