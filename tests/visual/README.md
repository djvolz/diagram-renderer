# Visual Regression Testing

This directory contains the visual regression testing system for diagram examples. It automatically captures screenshots of rendered diagrams and compares them against baseline reference images to detect visual changes.

## Quick Start

### 1. Generate Baseline Images (First Time Setup)
```bash
# Generate reference images for all working examples
python tests/visual/baseline_generator.py
```

### 2. Run Visual Tests
```bash
# Run complete visual regression test suite
python tests/visual/visual_test_runner.py

# Run with custom similarity threshold
python tests/visual/visual_test_runner.py --threshold 0.98

# Skip example regeneration (faster for development)
python tests/visual/visual_test_runner.py --skip-regen
```

### 3. Run via pytest
```bash
# Run visual regression tests through pytest
pytest tests/test_visual_regression.py -v

# Run only visual tests (requires baseline setup)
pytest -m visual
```

## How It Works

### Screenshot Capture
- Starts local HTTP server serving diagram examples
- Uses browser automation (Playwright preferred, fallback to browser MCP)
- Captures full-page screenshots at consistent 1200x800 resolution
- Waits for diagrams to fully render (detects zoom controls)

### Image Comparison
- **Fast comparison**: MD5 hash check for identical images
- **Detailed comparison**: Pixel-by-pixel analysis with similarity scoring
- **Visual diffs**: Generates highlighted diff images showing changes
- **Configurable thresholds**: Adjustable similarity requirements

### Test Organization
```
tests/visual/
├── baselines/              # Reference images (committed)
│   ├── mermaid/
│   │   ├── demo_flowchart.png
│   │   ├── demo_sequence_diagram.png
│   │   └── ...
│   ├── plantuml/
│   │   ├── plantuml_sequence_diagram.png
│   │   └── ...
│   └── graphviz/
│       ├── graphviz_directed_graph.png
│       └── ...
├── artifacts/              # Generated images (gitignored)
│   ├── current/           # Latest test run screenshots
│   ├── diffs/            # Visual diff images
│   └── visual_test_report_*.json
└── [test utilities]
```

## Usage Examples

### Updating Baselines (When Changes Are Expected)
```bash
# After making intentional visual changes, update baselines:
python tests/visual/baseline_generator.py

# Then commit the new baseline images:
git add tests/visual/baselines/
git commit -m "update visual baselines for improved styling"
```

### Investigating Failures
```bash
# Run tests and examine diff images
python tests/visual/visual_test_runner.py

# Check the generated diff images:
open tests/visual/artifacts/diffs/
```

### CI/CD Integration
```bash
# In CI, run visual tests without baseline generation:
python tests/visual/visual_test_runner.py --threshold 0.98
# Exit code 0 = all tests passed, exit code 1 = failures detected
```

## Configuration

### Similarity Thresholds
- **0.99**: Very strict (catches minor styling changes)
- **0.95**: Default (catches significant visual changes)
- **0.90**: Relaxed (only catches major rendering issues)

### Captured Examples
- **All working examples**: Only captures diagrams that render successfully
- **Excludes external/error diagrams**: Focuses on actual visual content
- **Consistent viewport**: 1200x800 resolution for all screenshots

## Dependencies

### Required
- `PIL (Pillow)`: Image comparison and diff generation
- `numpy`: Pixel-level image analysis

### Optional (but recommended)
- `playwright`: Fast, reliable screenshot capture
- Browser MCP: Fallback screenshot method

### Installation
```bash
# Install visual testing dependencies
uv add --group dev pillow numpy playwright

# Initialize Playwright browsers
playwright install chromium
```

## Integration with Existing Tests

### Test Markers
- `@pytest.mark.visual`: All visual regression tests
- `@pytest.mark.integration`: Tests requiring full system setup

### Running Different Test Types
```bash
# Run all tests including visual
pytest

# Run only unit tests (skip visual)
pytest -m "not visual"

# Run only visual tests
pytest -m visual

# Run with coverage
pytest --cov=diagram_renderer tests/
```

## Maintenance

### When to Update Baselines
- ✅ **Intentional visual improvements** (better styling, layout fixes)
- ✅ **New diagram features** that change appearance
- ✅ **Upgraded rendering libraries** with visual changes

### When NOT to Update Baselines
- ❌ **Rendering regressions** (black backgrounds, missing text)
- ❌ **Broken diagrams** showing error messages
- ❌ **Test failures** without understanding the cause

### Monitoring Visual Quality
1. **Automated CI checks** catch regressions before merge
2. **Manual review** of diff images for unexpected changes
3. **Baseline maintenance** when legitimate changes occur
4. **Threshold tuning** based on diagram complexity and requirements
