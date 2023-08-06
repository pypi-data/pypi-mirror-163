use pyo3::exceptions::PyRuntimeError;
use pyo3::prelude::*;

#[pyfunction]
fn get_query(where_query: String) -> PyResult<String> {
    let result = elastic_query::convert(where_query, 0, 100, vec![], vec![]);

    match result {
        Ok(value) => Ok(value.to_string()),
        Err(error) => {
            println!("{:?}", error);
            Err(PyRuntimeError::new_err(error.expected))
        }
    }
}

#[pymodule]
fn sql_to_query(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(get_query, m)?)?;
    Ok(())
}
