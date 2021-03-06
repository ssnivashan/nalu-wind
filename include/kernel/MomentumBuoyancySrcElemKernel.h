// Copyright 2017 National Technology & Engineering Solutions of Sandia, LLC
// (NTESS), National Renewable Energy Laboratory, University of Texas Austin,
// Northwest Research Associates. Under the terms of Contract DE-NA0003525
// with NTESS, the U.S. Government retains certain rights in this software.
//
// This software is released under the BSD 3-clause license. See LICENSE file
// for more details.
//


#ifndef MOMENTUMBUOYANCYSRCELEMKERNEL_H
#define MOMENTUMBUOYANCYSRCELEMKERNEL_H

#include "kernel/Kernel.h"
#include "FieldTypeDef.h"

#include <stk_mesh/base/BulkData.hpp>
#include <stk_mesh/base/Entity.hpp>

#include <Kokkos_Core.hpp>

namespace sierra {
namespace nalu {

class SolutionOptions;
class MasterElement;
class ElemDataRequests;

/** CMM buoyancy term for momentum equation (velocity DOF)
 */
template<typename AlgTraits>
class MomentumBuoyancySrcElemKernel: public NGPKernel<MomentumBuoyancySrcElemKernel<AlgTraits>>
{
public:
  MomentumBuoyancySrcElemKernel(
    const stk::mesh::BulkData&,
    const SolutionOptions&,
    ElemDataRequests&);

  KOKKOS_FUNCTION MomentumBuoyancySrcElemKernel() = default;
  KOKKOS_FUNCTION virtual ~MomentumBuoyancySrcElemKernel() = default;

  /** Execute the kernel within a Kokkos loop and populate the LHS and RHS for
   *  the linear solve
   */
  using Kernel::execute;

  KOKKOS_FUNCTION
  virtual void execute(
    SharedMemView<DoubleType**, DeviceShmem>&,
    SharedMemView<DoubleType*, DeviceShmem>&,
    ScratchViews<DoubleType, DeviceTeamHandleType, DeviceShmem>&);

private:
  unsigned densityNp1_ {stk::mesh::InvalidOrdinal};
  unsigned coordinates_ {stk::mesh::InvalidOrdinal};

  double rhoRef_;
  NALU_ALIGNED DoubleType gravity_[3];

  MasterElement* meSCV_{nullptr};
};

}  // nalu
}  // sierra

#endif /* MOMENTUMBUOYANCYSRCELEMKERNEL_H */
