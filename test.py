# Test if the images are loading correctly
try:
    idle = [tk.PhotoImage(file=impath + 'idle.gif', format='gif -index %i' % i) for i in range(5)]
    print("Idle images loaded successfully!")
except Exception as e:
    print(f"Error loading idle images: {e}")