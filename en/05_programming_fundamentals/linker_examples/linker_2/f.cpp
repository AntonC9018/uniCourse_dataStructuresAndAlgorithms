// Global non-static variable *definition*.
// Defining it again in another file will give a linker error
// (due to multiple definitions).
int a;

// This one exists only in this compilation unit / object file.
static int b;