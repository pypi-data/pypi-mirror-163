#[macro_use]
extern crate lazy_static;

use pyo3::prelude::*;

pub mod error;
pub mod extractors;
pub mod misc;
pub mod models;

use models::rich_text::{RichText, RichTextElement};
use models::table::{Cell, Row, Table};

#[pymodule]
fn rsoup(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_class::<Table>()?;
    m.add_class::<Row>()?;
    m.add_class::<Cell>()?;
    m.add_class::<RichText>()?;
    m.add_class::<RichTextElement>()?;
    m.add_class::<self::extractors::table::TableExtractor>()?;
    m.add_class::<self::extractors::context_v1::ContextExtractor>()?;
    m.add_class::<self::extractors::Document>()?;
    Ok(())
}
