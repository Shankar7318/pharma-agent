import pandas as pd
from typing import Dict, List, Any, Optional
import json
import random
from datetime import datetime, timedelta
import os

class MockPharmaAPIs:
    """Enhanced Mock APIs for pharmaceutical data sources with comprehensive sample data"""
    
    # Sample molecule database
    MOLECULE_DATABASE = {
        "ivermectin": {
            "generic_name": "Ivermectin",
            "brand_names": ["Stromectol", "Soolantra", "Ivomec"],
            "therapeutic_class": "Antiparasitic",
            "original_indication": "Parasitic infections",
            "mechanism": "GABA agonist",
            "molecular_weight": "875.1 g/mol",
            "repurposing_potential": "High"
        },
        "metformin": {
            "generic_name": "Metformin",
            "brand_names": ["Glucophage", "Fortamet", "Glumetza"],
            "therapeutic_class": "Antidiabetic",
            "original_indication": "Type 2 diabetes",
            "mechanism": "AMPK activation",
            "molecular_weight": "165.6 g/mol",
            "repurposing_potential": "Very High"
        },
        "remdesivir": {
            "generic_name": "Remdesivir",
            "brand_names": ["Veklury"],
            "therapeutic_class": "Antiviral",
            "original_indication": "COVID-19",
            "mechanism": "RNA polymerase inhibitor",
            "molecular_weight": "602.6 g/mol",
            "repurposing_potential": "Medium"
        }
    }
    
    @staticmethod
    def iqvia_market_data(therapy_area: str) -> Dict[str, Any]:
        """Enhanced Mock IQVIA market data API with realistic data"""
        base_data = {
            "respiratory": {
                "market_size": "2.1B", 
                "cagr": "8.2%", 
                "competitors": 12,
                "growth_drivers": ["Aging population", "Pollution", "Lifestyle factors"],
                "key_players": ["GSK", "AstraZeneca", "Novartis"],
                "therapy_breakdown": {
                    "Asthma": {"market_share": "35%", "growth": "6.5%"},
                    "COPD": {"market_share": "28%", "growth": "9.1%"},
                    "COVID-19": {"market_share": "15%", "growth": "12.3%"}
                }
            },
            "oncology": {
                "market_size": "15.3B", 
                "cagr": "12.7%", 
                "competitors": 45,
                "growth_drivers": ["Innovative therapies", "Early diagnosis", "Personalized medicine"],
                "key_players": ["Roche", "Merck", "Bristol-Myers Squibb"],
                "therapy_breakdown": {
                    "Immunotherapy": {"market_share": "42%", "growth": "18.5%"},
                    "Targeted Therapy": {"market_share": "35%", "growth": "14.2%"},
                    "Chemotherapy": {"market_share": "23%", "growth": "2.1%"}
                }
            },
            "cardiology": {
                "market_size": "8.7B", 
                "cagr": "6.8%", 
                "competitors": 28,
                "growth_drivers": ["Sedentary lifestyle", "Dietary habits", "Hypertension prevalence"],
                "key_players": ["Pfizer", "Novartis", "Bayer"],
                "therapy_breakdown": {
                    "Anticoagulants": {"market_share": "32%", "growth": "7.8%"},
                    "Beta-blockers": {"market_share": "25%", "growth": "3.2%"},
                    "ACE Inhibitors": {"market_share": "18%", "growth": "4.5%"}
                }
            }
        }
        
        data = base_data.get(therapy_area.lower(), {})
        
        # Extract sample data as DataFrame
        if data and 'therapy_breakdown' in data:
            therapy_df = pd.DataFrame.from_dict(data['therapy_breakdown'], orient='index')
            therapy_df.reset_index(inplace=True)
            therapy_df.columns = ['Therapy', 'Market_Share', 'Growth_Rate']
            data['therapy_dataframe'] = therapy_df.to_dict('records')
        
        return data
    
    @staticmethod
    def clinical_trials_search(molecule: str, indication: str = None) -> Dict[str, Any]:
        """Enhanced Clinical Trials API with realistic trial data"""
        
        trials_database = {
            "ivermectin": [
                {
                    "nct_id": "NCT04834115",
                    "phase": "Phase 3", 
                    "indication": "COVID-19", 
                    "status": "Completed",
                    "completion_date": "2022-08-31",
                    "sponsor": "University of Oxford",
                    "participants": 1500,
                    "primary_endpoint": "Mortality reduction",
                    "results": "No significant benefit observed",
                    "repurposing_potential": "Low"
                }
            ],
            "metformin": [
                {
                    "nct_id": "NCT04129957",
                    "phase": "Phase 3", 
                    "indication": "Breast Cancer", 
                    "status": "Active, not recruiting",
                    "completion_date": "2024-03-31",
                    "sponsor": "Dana-Farber Cancer Institute",
                    "participants": 3270,
                    "primary_endpoint": "Disease-free survival",
                    "results": "Preliminary: 15% improvement in DFS",
                    "repurposing_potential": "High"
                }
            ],
            "remdesivir": [
                {
                    "nct_id": "NCT04280705",
                    "phase": "Phase 3", 
                    "indication": "COVID-19", 
                    "status": "Completed",
                    "completion_date": "2022-05-20",
                    "sponsor": "Gilead Sciences",
                    "participants": 1062,
                    "primary_endpoint": "Recovery time",
                    "results": "5-day faster recovery vs placebo",
                    "repurposing_potential": "Medium"
                }
            ]
        }
        
        molecule_trials = trials_database.get(molecule.lower(), [])
        
        # Filter by indication if provided
        if indication:
            molecule_trials = [trial for trial in molecule_trials if indication.lower() in trial['indication'].lower()]
        
        # Extract sample data
        trials_df = pd.DataFrame(molecule_trials)
        summary_stats = {
            "total_trials": len(molecule_trials),
            "phases": trials_df['phase'].value_counts().to_dict() if not trials_df.empty else {},
            "status_distribution": trials_df['status'].value_counts().to_dict() if not trials_df.empty else {},
            "avg_participants": trials_df['participants'].mean() if not trials_df.empty else 0
        }
        
        return {
            "active_trials": molecule_trials,
            "total_trials": len(molecule_trials),
            "summary": f"Found {len(molecule_trials)} clinical trials for {molecule}",
            "summary_statistics": summary_stats,
            "trials_dataframe": trials_df.to_dict('records') if not trials_df.empty else [],
            "repurposing_opportunities": [trial for trial in molecule_trials if trial.get('repurposing_potential') in ['High', 'Medium']]
        }
    
    @staticmethod
    def patent_search(molecule: str) -> Dict[str, Any]:
        """Enhanced Patent API with realistic patent data"""
        
        patent_database = {
            "ivermectin": [
                {
                    "id": "US20210000000A1", 
                    "title": "Use of Ivermectin in Treatment of Respiratory Diseases", 
                    "expiry": "2035-12-31",
                    "status": "Active",
                    "assignee": "Pharma Innovations Inc.",
                    "filing_date": "2021-01-15",
                    "jurisdiction": "USA",
                    "claims": 25,
                    "citation_count": 45
                }
            ],
            "metformin": [
                {
                    "id": "US20220000000A1",
                    "title": "Metformin for Cancer Treatment and Prevention",
                    "expiry": "2040-05-15", 
                    "status": "Pending",
                    "assignee": "OncoResearch Foundation",
                    "filing_date": "2022-02-28",
                    "jurisdiction": "USA",
                    "claims": 42,
                    "citation_count": 67
                }
            ]
        }
        
        patents = patent_database.get(molecule.lower(), [])
        patents_df = pd.DataFrame(patents)
        
        # Patent analytics
        patent_stats = {
            "total_patents": len(patents),
            "active_patents": len([p for p in patents if p['status'] == 'Active']),
            "pending_patents": len([p for p in patents if p['status'] == 'Pending']),
            "avg_claims": patents_df['claims'].mean() if not patents_df.empty else 0,
            "total_citations": patents_df['citation_count'].sum() if not patents_df.empty else 0,
            "jurisdiction_distribution": patents_df['jurisdiction'].value_counts().to_dict() if not patents_df.empty else {}
        }
        
        return {
            "patents": patents,
            "total_patents": len(patents),
            "patent_statistics": patent_stats,
            "patents_dataframe": patents_df.to_dict('records') if not patents_df.empty else [],
            "freedom_to_operate": "Favorable" if len(patents) < 5 else "Moderate",
            "recommendations": [
                "File method-of-use patents for new indications",
                "Explore formulation patents for improved delivery",
                "Consider licensing opportunities for expiring patents"
            ]
        }
    
    @staticmethod
    def exim_trade_data(molecule: str, country: str = None) -> Dict[str, Any]:
        """Enhanced EXIM trade data API with realistic trade data"""
        
        trade_database = {
            "ivermectin": {
                "export_data": [
                    {"country": "USA", "volume_kg": 15000, "value_usd": 4500000, "year": 2023},
                    {"country": "Germany", "volume_kg": 8000, "value_usd": 2400000, "year": 2023}
                ],
                "import_data": [
                    {"country": "China", "volume_kg": 12000, "value_usd": 3000000, "year": 2023},
                    {"country": "India", "volume_kg": 9000, "value_usd": 2250000, "year": 2023}
                ]
            },
            "metformin": {
                "export_data": [
                    {"country": "USA", "volume_kg": 50000, "value_usd": 7500000, "year": 2023},
                    {"country": "UK", "volume_kg": 25000, "value_usd": 3750000, "year": 2023}
                ],
                "import_data": [
                    {"country": "India", "volume_kg": 40000, "value_usd": 5000000, "year": 2023},
                    {"country": "China", "volume_kg": 35000, "value_usd": 4375000, "year": 2023}
                ]
            }
        }
        
        molecule_data = trade_database.get(molecule.lower(), {"export_data": [], "import_data": []})
        
        # Filter by country if provided
        if country:
            export_data = [item for item in molecule_data["export_data"] if item["country"].lower() == country.lower()]
            import_data = [item for item in molecule_data["import_data"] if item["country"].lower() == country.lower()]
        else:
            export_data = molecule_data["export_data"]
            import_data = molecule_data["import_data"]
        
        # Create DataFrames for analysis
        export_df = pd.DataFrame(export_data)
        import_df = pd.DataFrame(import_data)
        
        # Trade analytics
        total_export_value = export_df['value_usd'].sum() if not export_df.empty else 0
        total_import_value = import_df['value_usd'].sum() if not import_df.empty else 0
        trade_balance = total_export_value - total_import_value
        
        return {
            "export_data": export_data,
            "import_data": import_data,
            "export_dataframe": export_df.to_dict('records'),
            "import_dataframe": import_df.to_dict('records'),
            "trade_analytics": {
                "total_export_value": total_export_value,
                "total_import_value": total_import_value,
                "trade_balance": trade_balance,
                "trade_balance_status": "Positive" if trade_balance > 0 else "Negative",
                "top_export_markets": export_df.nlargest(3, 'value_usd').to_dict('records') if not export_df.empty else [],
                "top_import_sources": import_df.nlargest(3, 'value_usd').to_dict('records') if not import_df.empty else []
            },
            "growth_trend": "Increasing" if total_export_value > 1000000 else "Stable"
        }
    
    @staticmethod
    def generate_repurposing_analysis(molecule: str, target_therapy: str) -> Dict[str, Any]:
        """Generate comprehensive repurposing analysis"""
        molecule_info = MockPharmaAPIs.MOLECULE_DATABASE.get(molecule.lower(), {})
        
        # Mock repurposing feasibility analysis
        feasibility_score = random.randint(60, 95)
        development_timeline = random.randint(2, 7)
        
        return {
            "molecule": molecule_info,
            "target_therapy": target_therapy,
            "repurposing_analysis": {
                "feasibility_score": feasibility_score,
                "development_timeline_years": development_timeline,
                "estimated_rd_cost_millions": random.randint(50, 500),
                "regulatory_pathway": "505(b)(2)" if feasibility_score > 70 else "IND",
                "key_advantages": [
                    "Established safety profile",
                    "Known pharmacokinetics",
                    "Existing manufacturing capability"
                ],
                "potential_challenges": [
                    "Patent limitations",
                    "Dosing optimization required",
                    "Competitive landscape"
                ],
                "recommended_actions": [
                    "Conduct preclinical studies",
                    "File method-of-use patents",
                    "Explore partnership opportunities"
                ]
            },
            "commercial_potential": {
                "addressable_population_millions": random.randint(10, 100),
                "peak_sales_potential_millions": random.randint(500, 2000),
                "time_to_peak_sales_years": development_timeline + 3
            }
        }


class EnhancedMockPharmaAPIs(MockPharmaAPIs):
    """Enhanced APIs with JSON data integration and advanced analytics"""
    
    def __init__(self):
        super().__init__()
        self.load_json_data()
    
    def load_json_data(self):
        """Load data from JSON files"""
        try:
            # Load molecules data
            molecules_path = os.path.join('data', 'molecules.json')
            if os.path.exists(molecules_path):
                with open(molecules_path, 'r') as f:
                    self.molecules_data = json.load(f)
            else:
                self.molecules_data = {"pharmaceutical_molecules": []}
            
            # Load patents data  
            patents_path = os.path.join('data', 'patents.json')
            if os.path.exists(patents_path):
                with open(patents_path, 'r') as f:
                    self.patents_data = json.load(f)
            else:
                self.patents_data = {"pharmaceutical_patents": []}
                
            # Load clinical trials data
            trials_path = os.path.join('data', 'clinical_trials.json')
            if os.path.exists(trials_path):
                with open(trials_path, 'r') as f:
                    self.trials_data = json.load(f)
            else:
                self.trials_data = {"clinical_trials": []}
                
        except Exception as e:
            print(f"Warning: JSON data loading failed: {e}")
            self.molecules_data = {"pharmaceutical_molecules": []}
            self.patents_data = {"pharmaceutical_patents": []}
            self.trials_data = {"clinical_trials": []}
    
    def get_molecule_details(self, molecule_name: str) -> dict:
        """Get detailed molecule information from JSON data"""
        for molecule in self.molecules_data.get("pharmaceutical_molecules", []):
            if molecule["generic_name"].lower() == molecule_name.lower():
                return molecule
        return {}
    
    def get_molecule_patents(self, molecule_name: str) -> list:
        """Get all patents for a specific molecule"""
        molecule_patents = []
        for patent in self.patents_data.get("pharmaceutical_patents", []):
            if patent["molecule"].lower() == molecule_name.lower():
                molecule_patents.append(patent)
        return molecule_patents
    
    def get_patent_landscape(self, molecule_name: str) -> dict:
        """Get comprehensive patent landscape for a molecule"""
        molecule_details = self.get_molecule_details(molecule_name)
        patents = self.get_molecule_patents(molecule_name)
        
        # Calculate patent metrics
        active_patents = len([p for p in patents if p.get("legal_status") == "Active"])
        pending_patents = len([p for p in patents if p.get("legal_status") == "Pending"])
        
        return {
            "molecule": molecule_details,
            "patents": patents,
            "patent_metrics": {
                "total_patents": len(patents),
                "active_patents": active_patents,
                "pending_patents": pending_patents,
                "coverage_years": self._calculate_patent_coverage(patents)
            },
            "freedom_to_operate": self._assess_fto_landscape(patents),
            "white_space_opportunities": self._identify_white_space(molecule_name, patents)
        }
    
    def _calculate_patent_coverage(self, patents: list) -> dict:
        """Calculate patent coverage timeline"""
        if not patents:
            return {"coverage_until": "No patents", "gap_years": 0}
        
        expiry_dates = [p.get("expiry_date") for p in patents if p.get("expiry_date")]
        if expiry_dates:
            latest_expiry = max(expiry_dates)
            return {"coverage_until": latest_expiry, "gap_years": 5}  # Mock gap calculation
        return {"coverage_until": "Unknown", "gap_years": 0}
    
    def _assess_fto_landscape(self, patents: list) -> str:
        """Assess overall freedom to operate landscape"""
        if not patents:
            return "Favorable"
        
        risks = [p.get("freedom_to_operate_analysis", {}).get("infringement_risk", "Low") 
                for p in patents]
        if any(risk == "High" for risk in risks):
            return "Challenging"
        elif any(risk == "Medium" for risk in risks):
            return "Moderate"
        return "Favorable"
    
    def _identify_white_space(self, molecule_name: str, existing_patents: list) -> list:
        """Identify white space opportunities"""
        opportunities = [
            "Combination therapies with newer agents",
            "Pediatric formulations", 
            "Novel delivery mechanisms",
            "Digital health integrations",
            "Personalized medicine approaches"
        ]
        
        # Filter based on existing patents
        patent_types = set(p.get("patent_type", "") for p in existing_patents)
        if "Formulation" not in patent_types:
            opportunities.append("Advanced formulation technologies")
        if "Method-of-use" not in patent_types:
            opportunities.append("New therapeutic methods and uses")
            
        return opportunities

    def get_enhanced_clinical_trials(self, molecule: str, max_results: int = 10) -> Dict[str, Any]:
        """Enhanced clinical trials search with JSON data integration"""
        # First try to get data from JSON
        json_trials = []
        for trial in self.trials_data.get("clinical_trials", []):
            if trial.get("molecule", "").lower() == molecule.lower():
                json_trials.append(trial)
        
        # If no JSON data, fall back to mock data
        if not json_trials:
            return self.clinical_trials_search(molecule)
        
        # Limit results
        json_trials = json_trials[:max_results]
        
        # Create DataFrame for analysis
        trials_df = pd.DataFrame(json_trials)
        
        # Enhanced analytics
        summary_stats = {
            "total_trials": len(json_trials),
            "phases": trials_df['phase'].value_counts().to_dict() if not trials_df.empty else {},
            "status_distribution": trials_df['status'].value_counts().to_dict() if not trials_df.empty else {},
            "sponsor_distribution": trials_df['sponsor'].value_counts().to_dict() if not trials_df.empty else {},
            "completion_timeline": self._analyze_trial_timeline(json_trials)
        }
        
        return {
            "active_trials": json_trials,
            "total_trials": len(json_trials),
            "summary_statistics": summary_stats,
            "trials_dataframe": trials_df.to_dict('records') if not trials_df.empty else [],
            "repurposing_opportunities": [trial for trial in json_trials if trial.get('repurposing_potential') in ['High', 'Medium']],
            "data_source": "JSON Database"
        }
    
    def _analyze_trial_timeline(self, trials: list) -> dict:
        """Analyze clinical trial completion timeline"""
        if not trials:
            return {}
        
        completion_dates = [trial.get('completion_date') for trial in trials if trial.get('completion_date')]
        if completion_dates:
            try:
                dates = [datetime.strptime(date, '%Y-%m-%d') for date in completion_dates]
                upcoming = [date for date in dates if date > datetime.now()]
                return {
                    "upcoming_completions": len(upcoming),
                    "next_completion": min(upcoming).strftime('%Y-%m-%d') if upcoming else "None",
                    "completed_trials": len(dates) - len(upcoming)
                }
            except:
                return {}
        return {}