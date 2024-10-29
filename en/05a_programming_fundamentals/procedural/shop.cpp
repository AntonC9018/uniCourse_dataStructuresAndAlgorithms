#include <iostream>
#include <string_view>
#include <span>

struct Item
{
    int price;
    std::string_view title;
    std::string_view brand;
};

struct Customer
{
    int moneyLeft;
    std::span<int> boughtItems;
};

void printItems(std::span<const Item> items)
{
    for (size_t i = 0; i < items.size(); i++)
    {
        const Item& item = items[i];
        std::cout 
            << (i + 1)
            << ". "
            << item.title
            << " from "
            << item.brand
            << " for "
            << item.price
            << std::endl;
    }
}

struct ShopCycleContext
{
    std::span<const Item> items;
    Customer* customer;
};

bool tryBuyItem(ShopCycleContext context, size_t itemIndex)
{
    const Item& item = context.items[itemIndex];
    if (context.customer->moneyLeft < item.price)
    {
        return false;
    }

    context.customer->boughtItems[itemIndex] += 1;
    return true;
}

void processCustomer(ShopCycleContext context)
{
    while (true)
    {
        printItems(context.items);
        std::cout << "You have " << context.customer->moneyLeft << " money left" << std::endl;
        std::cout << "Enter the number of the item to buy, or 0 to exit: " << std::endl;

        size_t choice;
        std::cin >> choice;

        if (choice == 0)
        {
            break;
        }

        size_t itemIndex = choice - 1;
        if (itemIndex >= context.items.size())
        {
            std::cout << "Invalid option." << std::endl;
            continue;
        }

        bool itemBought = tryBuyItem(context, itemIndex);
        if (itemBought)
        {
            const Item& item = context.items[itemIndex];
            std::cout << item.title << " has been added";
        }
        else
        {
            std::cout << "Not enough money" << std::endl;
        }
    }

    std::cout << "You have bought: " << std::endl;
    for (size_t i = 0; i < context.items.size(); i++)
    {
        const int& boughtCount = context.customer->boughtItems[i];
        if (boughtCount > 0)
        {
            const Item& item = context.items[i];
            std::cout 
                << boughtCount 
                << " of "
                << item.title
                << " from "
                << item.brand
                << std::endl;
        }
    }
}

int main()
{
    std::array items{
        Item{
            .price = 50,
            .title = "Retail Sneakers",
            .brand = "Nike",
        },
        Item{
            .price = 20,
            .title = "Blue blouse",
            .brand = "Sample1",
        },
        Item{
            .price = 10,
            .title = "Unisex Hat",
            .brand = "Lucoil",
        },
    };

    std::array<int, items.size()> boughtMemory{};
    Customer customer{
        .moneyLeft = 100,
        .boughtItems = boughtMemory,
    };

    processCustomer({
        .items = items,
        .customer = &customer
    });
}
