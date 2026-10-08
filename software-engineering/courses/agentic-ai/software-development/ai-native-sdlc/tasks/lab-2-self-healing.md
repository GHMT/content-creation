# Lab 2: Self-Healing Test Loops

## 🎯 Learning Objectives
*   Implement Test-Driven Development (TDD) in an AI-Native context.
*   Establish a feedback loop where agent code edits are driven by test outputs.
*   Handle compiler errors and unit test logs programmatically.

---

## 🛠️ The Scenario
You are building a **Shopping Cart Calculator**. It needs to calculate the total cost of items in the cart, apply a percentage discount, and add a location-based tax rate.

Instead of writing the calculator code yourself, you will write a complete, failing test suite first. Then, you will instruct the AI agent to write the calculator code and iterate until all tests run green.

---

## 📝 Part 1: Write the Failing Test Suite
Create a test file `tests/cartCalculator.test.ts` with assertions checking:
1.  **Subtotal Calculation**: Multiplies quantities by item prices.
2.  **Discounts**: Applies a discount code (e.g., `SAVE10` gives 10% off the subtotal).
3.  **Taxes**: Applies tax to the *discounted* subtotal.
4.  **Edge Cases**: Zero items, negative prices (should throw an error), invalid discount codes.

### Example test block:
```typescript
import { calculateCartTotal } from '../src/cartCalculator';

test('calculates correct total with discount and tax', () => {
    const items = [
        { price: 100, quantity: 2 }, // 200
        { price: 50, quantity: 1 }   // 50 -> subtotal 250
    ];
    const result = calculateCartTotal(items, 'SAVE10', 0.10); // 10% tax
    // 250 - 10% (25) = 225. 225 + 10% tax (22.5) = 247.5
    expect(result.total).toBe(247.5);
});
```

Run `npm test` and verify that the test suite fails (e.g. because `calculateCartTotal` doesn't exist yet).

---

## 🤖 Part 2: Kick off the Self-Healing Loop
1.  Open your agent tool / command runner.
2.  Give the agent access to compile and run tests.
3.  Instruct the agent:
    ```
    "The test file at @tests/cartCalculator.test.ts is currently failing. Your goal is to:
     1. Create src/cartCalculator.ts.
     2. Write the implementation.
     3. Run 'npm test' in the terminal.
     4. Read the failures (if any), adjust your code, and run tests again.
     Repeat this loop until all tests pass."
    ```
4.  Observe the agent's behavior. Watch it modify the implementation file, parse the Jest terminal errors, locate its logic bugs, and re-run tests.

---

## 🔍 Part 3: Verify the Robustness
Once the tests are green:
1.  Add a new, tricky test case to the test file (e.g., fractional quantities or massive precision numbers).
2.  Run the agent again: *"I added a new test case. Run tests and self-heal if necessary."*
3.  Observe if the agent is able to refine its initial architecture without breaking existing tests.

---

## 💡 Lab Reflection Questions
*   How did the specific assertion error messages affect the speed of the agent's bug-fixing?
*   What happens to an agent if you have a "flaky" test that succeeds 50% of the time? How can we design tests to prevent this?
