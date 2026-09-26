"""Enable CLI and graphical entry points for the package."""

import sys

if "--gui" in sys.argv:
    sys.argv.remove("--gui")
    from .gui import main

    main()
else:
    from .cli import main

    raise SystemExit(main())
