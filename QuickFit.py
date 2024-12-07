class MemoryPool:
    def __init__(self, size, blocks):
        self.size = size
        self.blocks = blocks

    def allocate(self):
        # Allocate the first block from the pool if available
        if self.blocks:
            block = self.blocks.pop(0)
            return block
        return None


class MemoryAllocator:
    def __init__(self):
        # Initialize memory pools with the blocks available
        self.memory_pools = {
            30: MemoryPool(30, ["Block 1", "Block 2"]),
            60: MemoryPool(60, ["Block 3", "Block 4"]),
            120: MemoryPool(120, ["Block 5", "Block 6"]),
            240: MemoryPool(240, ["Block 7"]),
        }

    def allocate_memory(self, request_size):
        # Check if the requested size is available in the exact pool or a larger pool
        if request_size in self.memory_pools:
            pool = self.memory_pools[request_size]
            block = pool.allocate()
            return block
        else:
            # If exact size is not available, check larger pools
            for size in sorted(self.memory_pools.keys()):
                if size >= request_size:
                    pool = self.memory_pools[size]
                    block = pool.allocate()
                    return block
        return None

    def get_free_blocks(self):
        # Get the remaining free blocks in each pool
        return {size: pool.blocks for size, pool in self.memory_pools.items()}


# Initialize memory allocator
allocator = MemoryAllocator()

# Website allocation requests (sizes)
requests = [30, 50, 120, 200, 35]

# Allocate memory for each website
allocated_blocks = {}
for i, req_size in enumerate(requests):
    block = allocator.allocate_memory(req_size)
    if block:
        allocated_blocks[f"Website {chr(65 + i)}"] = (req_size, block)
    else:
        allocated_blocks[f"Website {chr(65 + i)}"] = (req_size, None)

# Get the free blocks in the pools
free_blocks = allocator.get_free_blocks()

# Final Memory State Output
print("Current Memory State:")

# Memory Pools
print("\nUpdated Memory Pools:")
for size, pool in allocator.memory_pools.items():
    print(f"  {size} KB Pool: {pool.blocks}")

# Allocated blocks
print("\nAllocated Blocks:")
for website, (size, block) in allocated_blocks.items():
    if block:
        print(f"  {website}: {size} KB ({block})")
    else:
        print(f"  {website}: {size} KB (No allocation)")

# Free blocks
print("\nFree Blocks:")
for size, blocks in free_blocks.items():
    for block in blocks:
        print(f"  {size} KB: {block}")
