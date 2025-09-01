import streamlit as st
import pandas as pd
from datetime import datetime
import base64

# Page configuration
st.set_page_config(
    page_title="StyleHub - Fashion Store",
    page_icon="👗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2E8B57;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .category-header {
        color: #4A4A4A;
        font-size: 2rem;
        font-weight: bold;
        margin: 1rem 0;
        border-bottom: 2px solid #2E8B57;
        padding-bottom: 0.5rem;
    }
    
    .product-card {
        border: 1px solid #E0E0E0;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: transform 0.2s;
    }
    
    .product-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    
    .price-tag {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2E8B57;
    }
    
    .discount-price {
        color: #FF6B6B;
        text-decoration: line-through;
        font-size: 1rem;
    }
    
    .sale-badge {
        background-color: #FF6B6B;
        color: white;
        padding: 0.2rem 0.5rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    
    .new-badge {
        background-color: #4ECDC4;
        color: white;
        padding: 0.2rem 0.5rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for cart
if 'cart' not in st.session_state:
    st.session_state.cart = []

if 'cart_total' not in st.session_state:
    st.session_state.cart_total = 0

# Sample product data
@st.cache_data
def load_products():
    products = {
        "Men's Wear": [
            {"name": "Classic Denim Jacket", "price": 89.99, "original_price": 120.00, "size": ["S", "M", "L", "XL"], "color": ["Blue", "Black"], "status": "sale", "rating": 4.5, "image": "🧥"},
            {"name": "Cotton T-Shirt", "price": 24.99, "original_price": None, "size": ["S", "M", "L", "XL", "XXL"], "color": ["White", "Black", "Navy", "Gray"], "status": "new", "rating": 4.2, "image": "👕"},
            {"name": "Formal Shirt", "price": 45.99, "original_price": None, "size": ["S", "M", "L", "XL"], "color": ["White", "Blue", "Light Blue"], "status": "regular", "rating": 4.7, "image": "👔"},
            {"name": "Cargo Pants", "price": 65.99, "original_price": 85.00, "size": ["30", "32", "34", "36", "38"], "color": ["Khaki", "Black", "Olive"], "status": "sale", "rating": 4.3, "image": "👖"},
            {"name": "Sneakers", "price": 120.00, "original_price": None, "size": ["7", "8", "9", "10", "11", "12"], "color": ["White", "Black", "Gray"], "status": "new", "rating": 4.6, "image": "👟"},
        ],
        "Women's Wear": [
            {"name": "Summer Dress", "price": 79.99, "original_price": 100.00, "size": ["XS", "S", "M", "L", "XL"], "color": ["Floral", "Solid Blue", "Red"], "status": "sale", "rating": 4.8, "image": "👗"},
            {"name": "Silk Blouse", "price": 55.99, "original_price": None, "size": ["XS", "S", "M", "L"], "color": ["White", "Cream", "Pink"], "status": "new", "rating": 4.4, "image": "👚"},
            {"name": "High-Waist Jeans", "price": 68.99, "original_price": None, "size": ["26", "28", "30", "32", "34"], "color": ["Blue", "Black", "Light Blue"], "status": "regular", "rating": 4.6, "image": "👖"},
            {"name": "Blazer", "price": 95.99, "original_price": 130.00, "size": ["XS", "S", "M", "L", "XL"], "color": ["Black", "Navy", "Gray"], "status": "sale", "rating": 4.5, "image": "🧥"},
            {"name": "Heels", "price": 85.00, "original_price": None, "size": ["6", "7", "8", "9", "10"], "color": ["Black", "Nude", "Red"], "status": "regular", "rating": 4.3, "image": "👠"},
        ],
        "Kids": [
            {"name": "Cartoon T-Shirt", "price": 18.99, "original_price": None, "size": ["2T", "3T", "4T", "5T", "6T"], "color": ["Blue", "Pink", "Yellow"], "status": "new", "rating": 4.7, "image": "👕"},
            {"name": "Denim Overalls", "price": 32.99, "original_price": 45.00, "size": ["2T", "3T", "4T", "5T"], "color": ["Blue", "Light Blue"], "status": "sale", "rating": 4.4, "image": "👖"},
            {"name": "School Uniform", "price": 28.99, "original_price": None, "size": ["4", "6", "8", "10", "12"], "color": ["Navy", "White"], "status": "regular", "rating": 4.2, "image": "👔"},
            {"name": "Rain Jacket", "price": 25.99, "original_price": 35.00, "size": ["2T", "3T", "4T", "5T", "6T"], "color": ["Yellow", "Red", "Blue"], "status": "sale", "rating": 4.1, "image": "🧥"},
            {"name": "Kids Sneakers", "price": 35.00, "original_price": None, "size": ["7", "8", "9", "10", "11", "12"], "color": ["White", "Pink", "Blue"], "status": "new", "rating": 4.5, "image": "👟"},
        ],
        "Accessories": [
            {"name": "Leather Belt", "price": 29.99, "original_price": None, "size": ["S", "M", "L", "XL"], "color": ["Brown", "Black"], "status": "regular", "rating": 4.3, "image": "🔗"},
            {"name": "Sunglasses", "price": 45.99, "original_price": 65.00, "size": ["One Size"], "color": ["Black", "Brown", "Gold"], "status": "sale", "rating": 4.6, "image": "🕶️"},
            {"name": "Baseball Cap", "price": 22.99, "original_price": None, "size": ["One Size"], "color": ["Black", "Navy", "Red", "White"], "status": "new", "rating": 4.2, "image": "🧢"},
            {"name": "Leather Wallet", "price": 49.99, "original_price": None, "size": ["One Size"], "color": ["Brown", "Black"], "status": "regular", "rating": 4.8, "image": "👝"},
            {"name": "Watch", "price": 150.00, "original_price": 200.00, "size": ["One Size"], "color": ["Silver", "Gold", "Black"], "status": "sale", "rating": 4.7, "image": "⌚"},
        ]
    }
    return products

# Header
st.markdown('<h1 class="main-header">StyleHub Fashion Store</h1>', unsafe_allow_html=True)

# Sidebar for navigation and filters
with st.sidebar:
    st.header("🛍️ Navigation")
    
    # Navigation menu
    page = st.selectbox(
        "Choose a page:",
        ["Home", "Shop by Category", "Cart", "About Us"]
    )
    
    if page == "Shop by Category":
        st.subheader("🔍 Filters")
        
        # Category filter
        categories = ["All"] + list(load_products().keys())
        selected_category = st.selectbox("Category:", categories)
        
        # Price range filter
        price_range = st.slider("Price Range ($):", 0, 200, (0, 200))
        
        # Size filter
        all_sizes = set()
        for category_products in load_products().values():
            for product in category_products:
                all_sizes.update(product["size"])
        
        selected_sizes = st.multiselect("Size:", sorted(all_sizes))
        
        # Color filter
        all_colors = set()
        for category_products in load_products().values():
            for product in category_products:
                all_colors.update(product["color"])
        
        selected_colors = st.multiselect("Color:", sorted(all_colors))
        
        # Status filter
        status_options = ["All", "new", "sale", "regular"]
        selected_status = st.selectbox("Status:", status_options)

# Function to add item to cart
def add_to_cart(product_name, price, size, color):
    item = {
        "name": product_name,
        "price": price,
        "size": size,
        "color": color,
        "quantity": 1
    }
    st.session_state.cart.append(item)
    st.session_state.cart_total += price
    st.success(f"Added {product_name} to cart!")

# Function to display product card
def display_product_card(product, category):
    with st.container():
        st.markdown('<div class="product-card">', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            st.markdown(f'<div style="font-size: 4rem; text-align: center;">{product["image"]}</div>', unsafe_allow_html=True)
        
        with col2:
            st.subheader(product["name"])
            
            # Status badges
            if product["status"] == "sale":
                st.markdown('<span class="sale-badge">SALE</span>', unsafe_allow_html=True)
            elif product["status"] == "new":
                st.markdown('<span class="new-badge">NEW</span>', unsafe_allow_html=True)
            
            # Price display
            if product["original_price"]:
                st.markdown(f'<span class="price-tag">${product["price"]}</span> <span class="discount-price">${product["original_price"]}</span>', unsafe_allow_html=True)
            else:
                st.markdown(f'<span class="price-tag">${product["price"]}</span>', unsafe_allow_html=True)
            
            # Rating
            stars = "⭐" * int(product["rating"])
            st.write(f"{stars} ({product['rating']}/5)")
            
            # Available sizes and colors
            st.write(f"**Sizes:** {', '.join(product['size'])}")
            st.write(f"**Colors:** {', '.join(product['color'])}")
        
        with col3:
            st.write("**Select Options:**")
            selected_size = st.selectbox(f"Size", product["size"], key=f"size_{product['name']}_{category}")
            selected_color = st.selectbox(f"Color", product["color"], key=f"color_{product['name']}_{category}")
            
            if st.button(f"Add to Cart", key=f"cart_{product['name']}_{category}"):
                add_to_cart(product["name"], product["price"], selected_size, selected_color)
        
        st.markdown('</div>', unsafe_allow_html=True)

# Main content based on selected page
if page == "Home":
    st.markdown("### Welcome to StyleHub! 👋")
    st.write("Discover the latest fashion trends and timeless classics for everyone in the family.")
    
    # Featured products
    st.markdown('<h2 class="category-header">Featured Products</h2>', unsafe_allow_html=True)
    
    products = load_products()
    featured = []
    for category, items in products.items():
        # Get one featured item from each category
        featured.append((items[0], category))
    
    for product, category in featured:
        display_product_card(product, f"featured_{category}")

elif page == "Shop by Category":
    products = load_products()
    
    # Filter products based on selections
    if selected_category == "All":
        filtered_products = products
    else:
        filtered_products = {selected_category: products[selected_category]}
    
    # Apply filters
    for category, items in filtered_products.items():
        st.markdown(f'<h2 class="category-header">{category}</h2>', unsafe_allow_html=True)
        
        filtered_items = []
        for product in items:
            # Price filter
            if not (price_range[0] <= product["price"] <= price_range[1]):
                continue
            
            # Size filter
            if selected_sizes and not any(size in product["size"] for size in selected_sizes):
                continue
            
            # Color filter
            if selected_colors and not any(color in product["color"] for color in selected_colors):
                continue
            
            # Status filter
            if selected_status != "All" and product["status"] != selected_status:
                continue
            
            filtered_items.append(product)
        
        if filtered_items:
            for product in filtered_items:
                display_product_card(product, category)
        else:
            st.info("No products match your filters. Try adjusting your criteria.")

elif page == "Cart":
    st.markdown('<h2 class="category-header">Shopping Cart 🛒</h2>', unsafe_allow_html=True)
    
    if st.session_state.cart:
        # Display cart items
        for i, item in enumerate(st.session_state.cart):
            col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 2, 1])
            
            with col1:
                st.write(f"**{item['name']}**")
            with col2:
                st.write(f"Size: {item['size']}")
            with col3:
                st.write(f"Color: {item['color']}")
            with col4:
                st.write(f"${item['price']}")
            with col5:
                if st.button("❌", key=f"remove_{i}"):
                    st.session_state.cart_total -= item['price']
                    st.session_state.cart.pop(i)
                    st.experimental_rerun()
        
        # Cart summary
        st.markdown("---")
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f'<h3 style="text-align: right;">Total: <span class="price-tag">${st.session_state.cart_total:.2f}</span></h3>', unsafe_allow_html=True)
        with col2:
            if st.button("🛍️ Checkout", type="primary"):
                st.success("Thank you for your purchase! (This is a demo)")
                st.session_state.cart = []
                st.session_state.cart_total = 0
                st.experimental_rerun()
    else:
        st.info("Your cart is empty. Start shopping to add items!")
        if st.button("Continue Shopping"):
            st.experimental_rerun()

elif page == "About Us":
    st.markdown('<h2 class="category-header">About StyleHub</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.write("""
        **StyleHub** is your one-stop destination for fashion-forward clothing and accessories. 
        We believe that style is a form of self-expression, and everyone deserves to look and feel their best.
        
        ### Our Mission
        To provide high-quality, trendy, and affordable fashion for the entire family while delivering 
        exceptional customer service.
        
        ### What We Offer
        - **Men's Fashion**: From casual wear to formal attire
        - **Women's Fashion**: Trendy dresses, professional wear, and everyday essentials
        - **Kids' Clothing**: Comfortable and durable clothes for active children
        - **Accessories**: Complete your look with our selection of belts, bags, and jewelry
        
        ### Why Choose Us?
        - ✅ High-quality materials
        - ✅ Affordable prices
        - ✅ Fast shipping
        - ✅ Easy returns
        - ✅ Excellent customer service
        """)
    
    with col2:
        st.markdown("""
        ### Contact Us
        📧 **Email:** info@stylehub.com  
        📞 **Phone:** (555) 123-4567  
        📍 **Address:** 123 Fashion Ave, Style City, SC 12345  
        
        ### Business Hours
        **Monday - Friday:** 9:00 AM - 8:00 PM  
        **Saturday:** 10:00 AM - 6:00 PM  
        **Sunday:** 12:00 PM - 5:00 PM  
        
        ### Follow Us
        📘 Facebook  
        📷 Instagram  
        🐦 Twitter  
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p>© 2024 StyleHub Fashion Store. All rights reserved.</p>
    <p>Made with ❤️ using Streamlit</p>
</div>
""", unsafe_allow_html=True)