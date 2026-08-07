class LayoutEngine:
    
    PAGE_WIDTH = 595
    PAGE_HEIGHT = 842

    MARGIN = 35
    GAP = 18

    HEADER_HEIGHT = 110
    FOOTER_HEIGHT = 40

    def generate_layout(self, products):

        count = len(products)

        # -----------------------------
        # 1 Product
        # -----------------------------
        if count == 1:

            return [

                {
                    "x": 55,
                    "y": 120,
                    "width": 485,
                    "height": 600
                }

            ]

        # -----------------------------
        # 2 Products
        # -----------------------------
        if count == 2:

            return [

                {
                    "x": 35,
                    "y": 160,
                    "width": 245,
                    "height": 520
                },

                {
                    "x": 315,
                    "y": 160,
                    "width": 245,
                    "height": 520
                }

            ]

        # -----------------------------
        # 3 Products
        # Hero Layout
        # -----------------------------
        if count == 3:

            return [

                {
                    "x": 55,
                    "y": 420,
                    "width": 485,
                    "height": 260
                },

                {
                    "x": 35,
                    "y": 140,
                    "width": 245,
                    "height": 220
                },

                {
                    "x": 315,
                    "y": 140,
                    "width": 245,
                    "height": 220
                }

            ]

        # -----------------------------
        # 4 Products
        # Hero Layout
        # -----------------------------
        if count == 4:

            return [

                {
                    "x": 35,
                    "y": 380,
                    "width": 260,
                    "height": 320
                },

                {
                    "x": 315,
                    "y": 520,
                    "width": 245,
                    "height": 160
                },

                {
                    "x": 315,
                    "y": 330,
                    "width": 245,
                    "height": 160
                },

                {
                    "x": 315,
                    "y": 140,
                    "width": 245,
                    "height": 160
                }

            ]

        # -----------------------------
        # 5-6 Products
        # -----------------------------
        if count <= 6:

            layout = []

            card_w = 160
            card_h = 170

            start_x = 35
            start_y = 500

            for r in range(2):

                for c in range(3):

                    if len(layout) >= count:
                        break

                    layout.append(

                        {
                            "x": start_x + c * 182,
                            "y": start_y - r * 240,
                            "width": card_w,
                            "height": card_h
                        }

                    )

            return layout

        # -----------------------------
        # 7-9 Products
        # -----------------------------
        layout = []

        card_w = 165
        card_h = 120

        start_x = 30
        start_y = 560

        for r in range(3):

            for c in range(3):

                if len(layout) >= count:
                    break

                layout.append(

                    {
                        "x": start_x + c * 185,
                        "y": start_y - r * 180,
                        "width": card_w,
                        "height": card_h
                    }

                )

        return layout