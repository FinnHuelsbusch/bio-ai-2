use serde::{Deserialize, Serialize};

#[derive(Debug, Deserialize, Serialize)]
pub struct FunctionConfig {
    pub name: String,

    #[serde(default)]
    pub probability: Option<f64>,

    #[serde(default)]
    pub tournament_size: Option<u32>,

    #[serde(default)]
    pub tournament_probability: Option<f32>,

    #[serde(default)]
    pub elitism_percentage: Option<f64>,
}

#[derive(Debug, Deserialize, Serialize)]
pub struct Config {
    pub problem_instance: String,
    pub population_size: u64,
    pub number_of_generations: u64,
    pub parent_selection: FunctionConfig,
    pub crossovers: Vec<FunctionConfig>,
    pub mutations: Vec<FunctionConfig>,
    pub survivor_selection: FunctionConfig
    
}

pub fn initialize_config(file_path: &str) -> Config {
    let data = std::fs::read_to_string(file_path).expect("Unable to read file");
    let config: Config = serde_json::from_str(&data).expect("JSON was not well-formatted");
    config
}