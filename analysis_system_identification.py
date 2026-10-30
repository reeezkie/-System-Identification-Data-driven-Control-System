import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ============================================================
# 1. LOAD DATA
# ============================================================

filename = "fixdatadriven.csv"
data = pd.read_csv(filename)

t = data["t_ms"].values
u = data["u_duty"].values
y = data["y_speed"].values

Ts = 0.05  # Sample time = 50 ms

print("============================================================")
print("SYSTEM IDENTIFICATION - FIRST-ORDER ARX")
print("============================================================")
print(f"Jumlah data : {len(data)}")
print(f"Sample time : {Ts * 1000:.0f} ms")


# ============================================================
# 2. CONSTRUCT X AND Y MATRICES
# ============================================================

# Model: y[k] = a1*y[k-1] + b1*u[k-1]

Y = y[1:]

X = np.column_stack((
    y[:-1],
    u[:-1]
))

print("\nUkuran X :", X.shape)
print("Ukuran Y :", Y.shape)


# ============================================================
# 3. LEAST SQUARES ESTIMATION
# ============================================================

# theta = (X^T X)^(-1) X^T Y

XTX = X.T @ X
XTY = X.T @ Y

theta = np.linalg.inv(XTX) @ XTY

a1 = theta[0]
b1 = theta[1]

print("\n============================================================")
print("ESTIMATED ARX MODEL")
print("============================================================")

print(f"a1 = {a1:.10f}")
print(f"b1 = {b1:.10f}")

print("\nModel:")
print(f"y[k] = {a1:.10f} y[k-1] + {b1:.10f} u[k-1]")


# ============================================================
# 4. MODEL PREDICTION
# ============================================================

y_pred = X @ theta
error = Y - y_pred


# ============================================================
# 5. MODEL VALIDATION
# ============================================================

MSE = np.mean(error ** 2)
RMSE = np.sqrt(MSE)

SS_res = np.sum(error ** 2)
SS_tot = np.sum((Y - np.mean(Y)) ** 2)

R2 = 1 - (SS_res / SS_tot)

condition_number = np.linalg.cond(XTX)

print("\n============================================================")
print("MODEL VALIDATION")
print("============================================================")

print(f"MSE  = {MSE:.7f}")
print(f"RMSE = {RMSE:.7f} RPS")
print(f"R²   = {R2:.7f}")

print(f"Condition number = {condition_number:.4f}")


# ============================================================
# 6. PLOT MEASURED VS PREDICTED
# ============================================================

t_valid = t[1:]

plt.figure(figsize=(12, 6))

plt.plot(
    t_valid / 1000,
    Y,
    label="Measured Velocity"
)

plt.plot(
    t_valid / 1000,
    y_pred,
    label="Predicted Velocity"
)

plt.xlabel("Time (s)")
plt.ylabel("Velocity (RPS)")
plt.title("Measured vs Predicted Motor Velocity")
plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig(
    "measured_vs_predicted_velocity.png",
    dpi=300
)

plt.show()


# ============================================================
# 7. PLOT PRBS INPUT
# ============================================================

plt.figure(figsize=(12, 4))

plt.step(
    t / 1000,
    u,
    where="post"
)

plt.xlabel("Time (s)")
plt.ylabel("PWM Duty Cycle (%)")
plt.title("PRBS PWM Input Signal")
plt.grid(True)
plt.tight_layout()

plt.savefig(
    "prbs_input_signal.png",
    dpi=300
)

plt.show()


# ============================================================
# 8. SAVE PREDICTION RESULTS
# ============================================================

result = pd.DataFrame({
    "t_ms": t_valid,
    "measured_velocity": Y,
    "predicted_velocity": y_pred,
    "error": error
})

result.to_csv(
    "prediction_result.csv",
    index=False
)

print("\n============================================================")
print("ANALYSIS COMPLETE")
print("============================================================")
print("Output:")
print("- measured_vs_predicted_velocity.png")
print("- prbs_input_signal.png")
print("- prediction_result.csv")