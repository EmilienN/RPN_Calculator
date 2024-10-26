# RPN Calculator Project Structure

## Project Overview
A Flask-based REST API implementing a Reverse Polish Notation (RPN) calculator with stack management capabilities.

## Directory Structure
```
rpn-calculator/
├── api/
│   ├── __init__.py
│   ├── models.py           # API request/response models
│   └── routes.py          # API endpoints and controller
├── core/
│   ├── __init__.py
│   ├── calculator_operations.py    # Calculator workflow
│   ├── calculator_state.py         # Stack state management
│   └── rpn_calculator_core.py      # Core RPN implementation
├── tests/
│   ├── __init__.py
│   ├── test_calculator_components.py   # Unit tests for core
│   └── test_routes.py                  # API endpoint tests
└── main.py                # Application entry point
```

## Components Description

### API Layer (`api/`)
- **models.py**: Defines Flask-RestX models for API requests and responses
  - `CalculatorResponse`: Stack state representation
  - `PushRequest`: Value push request model

- **routes.py**: Implements REST endpoints and controller logic
  - Manages multiple calculator instances
  - Handles stack creation, manipulation, and deletion
  - Implements RPN operations

### Core Layer (`core/`)
- **calculator_operations.py**: Workflow orchestration
  - Bridges API and core calculator functionality
  - Manages operation execution

- **calculator_state.py**: State management
  - Maintains calculator stack state
  - Implements stack operations

- **rpn_calculator_core.py**: Core calculator implementation
  - Implements RPN operations (+, -, *, /)
  - Manages stack manipulation

### Tests (`tests/`)
- **test_calculator_components.py**: Core component tests
  - Tests for RPNCalculator class
  - Tests for CalculatorWorkflow class
  - Integration tests

- **test_routes.py**: API endpoint tests
  - Tests for all REST endpoints
  - Tests error handling

### Entry Point
- **main.py**: Application configuration and startup
  - Flask app initialization
  - API documentation setup (Swagger)
  - Server configuration

## API Endpoints

```
GET    /rpn/op              # List available operators
POST   /rpn/op/{op}/{id}    # Apply operator to stack
POST   /rpn/stack           # Create new stack
GET    /rpn/stack           # List all stacks
GET    /rpn/stack/{id}      # Get specific stack
POST   /rpn/stack/{id}      # Push value to stack
DELETE /rpn/stack/{id}      # Delete stack
DELETE /rpn/stack/{id}/pop  # Pop value from stack
```